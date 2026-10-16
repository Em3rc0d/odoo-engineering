import io
import json
import sys
from pathlib import Path
import unittest
from urllib.error import URLError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from nubefact_gateway import (
    CPEIdentity, prepare_standard_sale, interpret_nubefact_reply,
    NubefactGateway, LiveEmissionDisabled, SubmissionOutcomeUnknown, ProviderIdentityMismatch,
)

IDENTITY = CPEIdentity("20123456789", "01", "F001", 1)
SALE = {"issue_date": "2026-10-16", "buyer_doc_kind": "6", "buyer_doc_number": "20987654321",
        "buyer_name": "CLIENTE DEMOSTRACION SAC", "buyer_address": "Lima",
        "items": [{"sku": "SKU001", "description": "Producto ficticio", "quantity": 2, "unit_net": "50.00"}],
        "odoo_total": "118.00", "currency": "PEN", "tax_profile": "pe_igv_18_taxable"}
ROUTE = "https://demo.nubefact.com/api/v1/03989d1a-6c8c-4b71-b1cd-7d37001deaa0"
TOKEN = "x" * 48  # intentionally fake; NEVER use published/shared demo credentials


class FakeResponse:
    def __init__(self, body):
        self.body = io.BytesIO(json.dumps(body).encode())
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self, n): return self.body.read(n)


class FakeOpener:
    def __init__(self, reply=None, error=None):
        self.reply, self.error, self.calls = reply or {}, error, []
    def open(self, request, timeout):
        self.calls.append((request, timeout))
        if self.error: raise self.error
        return FakeResponse(self.reply)


class GatewayTests(unittest.TestCase):
    def test_basic_invoice_payload_and_fingerprint(self):
        prepared = prepare_standard_sale(IDENTITY, SALE)
        self.assertEqual(prepared.payload["total"], 118.0)
        self.assertEqual(prepared.payload["total_igv"], 18.0)
        self.assertEqual(prepared.payload["items"][0]["tipo_de_igv"], 1)
        self.assertEqual(prepared, prepare_standard_sale(IDENTITY, SALE))
        self.assertEqual(len(prepared.sha256), 64)

    def test_boleta_supported(self):
        identity = CPEIdentity("20123456789", "03", "B001", 123)
        sale = dict(SALE, buyer_doc_kind="1", buyer_doc_number="12345678")
        p = prepare_standard_sale(identity, sale)
        self.assertEqual(p.payload["tipo_de_comprobante"], 2)
        self.assertEqual(p.payload["cliente_tipo_de_documento"], 1)

    def test_invalid_payloads_fail_before_send(self):
        failures = [dict(SALE, odoo_total="119.00"), dict(SALE, buyer_doc_kind="1"),
                    dict(SALE, items=[]), dict(SALE, items=[dict(SALE["items"][0], quantity=0)]),
                    dict(SALE, items=[dict(SALE["items"][0], unit_net="NaN")]),
                    dict(SALE, currency="USD"), dict(SALE, tax_profile="exonerated"),
                    dict(SALE, items=[dict(SALE["items"][0], quantity=3, unit_net="0.01")], odoo_total="0.04")]
        for sale in failures:
            with self.subTest(sale=sale), self.assertRaises(ValueError):
                prepare_standard_sale(IDENTITY, sale)
        with self.assertRaises(ValueError): CPEIdentity("123", "01", "F001", 1)
        with self.assertRaises(ValueError): CPEIdentity("20123456789", "01", "B001", 1)
        with self.assertRaises(ValueError): CPEIdentity("20123456789", "07", "F001", 1)

    def test_explicit_authorization_and_no_network_by_default(self):
        op = FakeOpener({"aceptada_por_sunat": True})
        client = NubefactGateway(route=ROUTE, token=TOKEN, opener=op)
        with self.assertRaises(LiveEmissionDisabled):
            client.submit(prepare_standard_sale(IDENTITY, SALE), human_authorized=True)
        self.assertFalse(op.calls)
        client = NubefactGateway(route=ROUTE, token=TOKEN, enable_emission=True, opener=op)
        with self.assertRaises(LiveEmissionDisabled):
            client.submit(prepare_standard_sale(IDENTITY, SALE))
        self.assertFalse(op.calls)

    def test_host_url_guard_and_token_guard(self):
        for route in ["http://demo.nubefact.com/api/v1/abcdabcdabcd",
                      "https://demo.nubefact.com.evil.com/api/v1/abcdabcdabcd",
                      "https://demo.nubefact.com/api/v1/abcdabcdabcd?q=x",
                      "https://evil.com/api/v1/abcdabcdabcd"]:
            with self.subTest(route=route), self.assertRaises(ValueError):
                NubefactGateway(route=route, token=TOKEN)
        with self.assertRaises(ValueError): NubefactGateway(route=ROUTE, token="fake")

    def test_send_contract_mocked_only(self):
        op = FakeOpener({"serie": "F001", "numero": 1, "aceptada_por_sunat": True,
                         "sunat_responsecode": "0", "enlace_del_xml": "https://example.invalid/xml"})
        client = NubefactGateway(route=ROUTE, token=TOKEN, enable_emission=True, opener=op)
        result = client.submit(prepare_standard_sale(IDENTITY, SALE), human_authorized=True)
        self.assertEqual(result["status"], "provider_reports_accepted")
        self.assertTrue(result["has_xml_link"])
        request, timeout = op.calls[0]
        self.assertEqual(timeout, 20)
        self.assertEqual(request.get_method(), "POST")
        self.assertIn(b'"operacion": "generar_comprobante"', request.data)
        self.assertIn("token=", request.get_header("Authorization"))

    def test_ambiguous_failure_must_never_retry(self):
        op = FakeOpener(error=URLError("network down, perhaps sent"))
        client = NubefactGateway(route=ROUTE, token=TOKEN, enable_emission=True, opener=op)
        with self.assertRaises(SubmissionOutcomeUnknown) as ctx:
            client.submit(prepare_standard_sale(IDENTITY, SALE), human_authorized=True)
        self.assertEqual(len(op.calls), 1)
        self.assertNotIn("network down", str(ctx.exception))
        self.assertNotIn(TOKEN, str(ctx.exception))

    def test_response_identity_mismatch(self):
        op = FakeOpener({"serie": "F001", "numero": 2, "aceptada_por_sunat": True})
        client = NubefactGateway(route=ROUTE, token=TOKEN, enable_emission=True, opener=op)
        with self.assertRaises(ProviderIdentityMismatch):
            client.submit(prepare_standard_sale(IDENTITY, SALE), human_authorized=True)

    def test_unknown_is_not_accepted(self):
        self.assertEqual(interpret_nubefact_reply({}, IDENTITY)["status"], "unknown")
        self.assertEqual(interpret_nubefact_reply({"errors": "error", "aceptada_por_sunat": True}, IDENTITY)["status"], "provider_error")
        self.assertEqual(interpret_nubefact_reply({"aceptada_por_sunat": False, "sunat_responsecode": "123"}, IDENTITY)["status"], "needs_review")


if __name__ == "__main__":
    unittest.main()
