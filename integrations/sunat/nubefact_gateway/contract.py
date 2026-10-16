"""Pure, intentionally restricted Nubefact JSON payload and status contract.

Only 18% IGV, wholly taxable, one-currency local PEN sales (invoice/receipt).
No claim of full legal/business validation; customer-specific tax regimes vary.
Never derive transaction identity from a mutable UI session or provider response.
"""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from hashlib import sha256
import json
import re
from typing import Mapping

_MONEY = Decimal("0.01")
_TAX = Decimal("0.18")
_IDENT_RE = re.compile(r"^[0-9]{11}$")
_SERIES_RE = re.compile(r"^[FB][0-9A-Z]{3}$")
_TYPE = {"01": 1, "03": 2}  # invoice, boleta (notes handled in later gate)


@dataclass(frozen=True)
class CPEIdentity:
    issuer_ruc: str
    kind: str  # SUNAT 01 factura, 03 boleta
    series: str
    number: int

    def __post_init__(self):
        if not _IDENT_RE.fullmatch(self.issuer_ruc):
            raise ValueError("Issuer RUC must contain 11 digits")
        if self.kind not in _TYPE:
            raise ValueError("Only SUNAT 01/03 initial-sale documents supported")
        if not _SERIES_RE.fullmatch(self.series):
            raise ValueError("Series must contain F/B and three alphanumerics")
        if self.series[0] != ("F" if self.kind == "01" else "B"):
            raise ValueError("Series and document type mismatch")
        if type(self.number) is not int or not (1 <= self.number <= 99999999):
            raise ValueError("Invalid sequential document number")

    @property
    def key(self) -> str:
        return f"{self.issuer_ruc}:{self.kind}:{self.series}:{self.number}"


def _decimal(v, name: str, *, positive: bool = False) -> Decimal:
    try:
        if isinstance(v, (bool, float)) or v is None:
            raise ValueError
        d = Decimal(str(v))
        if not d.is_finite() or d < 0 or (positive and d <= 0):
            raise ValueError
        return d
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError(f"Invalid {name}") from None


def _money(v: Decimal) -> float:
    return float(v.quantize(_MONEY, rounding=ROUND_HALF_UP))


@dataclass(frozen=True)
class PreparedCPE:
    identity: CPEIdentity
    payload: dict
    sha256: str


def prepare_standard_sale(identity: CPEIdentity, sale: Mapping) -> PreparedCPE:
    """Build *candidate* provider JSON from an immutable, authorized invoice snapshot.

    Quantity restricted to positive integers; one 18% tax code, no discounts,
    free items, foreign currency, credit/debit notes, exports or perceptions.
    Does not alter Odoo/accounting records nor assign legal document numbers.
    """
    if not isinstance(sale, Mapping):
        raise ValueError("Expected sale mapping")
    if sale.get("currency") != "PEN" or sale.get("tax_profile") != "pe_igv_18_taxable":
        raise ValueError("Only explicitly classified PEN/18% taxable transactions supported")
    try:
        issue_date = date.fromisoformat(sale["issue_date"])
    except (KeyError, TypeError, ValueError):
        raise ValueError("Invalid ISO issue_date") from None
    doc_kind, buyer_id = sale.get("buyer_doc_kind"), sale.get("buyer_doc_number")
    if doc_kind not in ("1", "6") or not isinstance(buyer_id, str) or not buyer_id.isdigit():
        raise ValueError("Buyer ID type must be 1 (DNI) or 6 (RUC)")
    if len(buyer_id) != (8 if doc_kind == "1" else 11):
        raise ValueError("Invalid buyer document length")
    if identity.kind == "01" and doc_kind != "6":
        raise ValueError("Invoice requires RUC buyer for this supported workflow")
    name = sale.get("buyer_name")
    if not isinstance(name, str) or not name.strip() or len(name) > 250:
        raise ValueError("Buyer name required")
    address = sale.get("buyer_address", "")
    if not isinstance(address, str) or len(address) > 250:
        raise ValueError("Invalid buyer address")
    items = sale.get("items")
    if not isinstance(items, list) or not 1 <= len(items) <= 200:
        raise ValueError("One to 200 item lines required")
    rows, net_sum, tax_sum = [], Decimal("0"), Decimal("0")
    for i, item in enumerate(items):
        if not isinstance(item, Mapping):
            raise ValueError("Invalid item line")
        description = item.get("description")
        if not isinstance(description, str) or not description.strip() or len(description) > 250:
            raise ValueError(f"Invalid item {i} description")
        quantity = item.get("quantity")
        if type(quantity) is not int or not 1 <= quantity <= 100000:
            raise ValueError(f"Item {i} quantity must be a positive integer")
        unit_net = _decimal(item.get("unit_net"), f"item {i} unit_net", positive=True)
        if unit_net.as_tuple().exponent < -2:
            raise ValueError(f"Item {i} price supports max two decimal places")
        net = (unit_net * quantity).quantize(_MONEY, rounding=ROUND_HALF_UP)
        igv = (net * _TAX).quantize(_MONEY, rounding=ROUND_HALF_UP)
        total = net + igv
        if _money(unit_net * (Decimal("1") + _TAX)) * quantity != _money(total):
            raise ValueError(f"Item {i} requires a reviewed rounding allocation")
        net_sum += net
        tax_sum += igv
        code = item.get("sku", "")
        if not isinstance(code, str) or len(code) > 80:
            raise ValueError("Invalid SKU")
        rows.append({"unidad_de_medida": "NIU", "codigo": code,
                     "descripcion": description.strip(), "cantidad": quantity,
                     "valor_unitario": _money(unit_net),
                     "precio_unitario": _money(unit_net + (unit_net * _TAX)),
                     "subtotal": _money(net), "tipo_de_igv": 1,
                     "igv": _money(igv), "total": _money(total)})
    expected_total = _money(net_sum + tax_sum)
    stated_total = sale.get("odoo_total")
    if stated_total is None or _money(_decimal(stated_total, "odoo_total")) != expected_total:
        raise ValueError("Odoo total does not match independently computed amounts")
    payload = {
        "operacion": "generar_comprobante", "tipo_de_comprobante": _TYPE[identity.kind],
        "serie": identity.series, "numero": identity.number, "sunat_transaction": 1,
        "cliente_tipo_de_documento": int(doc_kind),
        "cliente_numero_de_documento": buyer_id,
        "cliente_denominacion": name.strip(), "cliente_direccion": address,
        "fecha_de_emision": issue_date.strftime("%d-%m-%Y"),
        "moneda": 1, "porcentaje_de_igv": 18.0,
        "total_gravada": _money(net_sum), "total_igv": _money(tax_sum),
        "total": expected_total, "items": rows,
        "enviar_automaticamente_a_la_sunat": True,
        "enviar_automaticamente_al_cliente": False,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return PreparedCPE(identity=identity, payload=payload, sha256=sha256(encoded).hexdigest())


def interpret_nubefact_reply(response: Mapping, identity: CPEIdentity) -> dict:
    """Conservative status projection: unknown is NOT success and HTTP 200 is NOT CDR.

    Keep full provider reply in access-controlled storage only after policy review.
    Never print raw replies containing potentially personal/tax information.
    """
    if not isinstance(response, Mapping):
        raise ValueError("Provider response must be an object")
    if response.get("errors"):
        status = "provider_error"
    elif response.get("aceptada_por_sunat") is True:
        status = "provider_reports_accepted"
    elif response.get("aceptada_por_sunat") is False and response.get("sunat_responsecode"):
        status = "needs_review"  # Not enough to assert final rejection
    else:
        status = "unknown"
    return {"identity": identity.key, "status": status,
            "sunat_responsecode": str(response.get("sunat_responsecode") or "")[:40],
            "has_cdr_link": bool(response.get("enlace_del_cdr")),
            "has_xml_link": bool(response.get("enlace_del_xml")),
            "has_pdf_link": bool(response.get("enlace_del_pdf"))}
