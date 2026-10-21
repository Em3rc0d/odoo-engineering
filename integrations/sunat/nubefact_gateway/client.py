"""Explicit-opt-in, NO-RETRY Nubefact JSON transport. Never sends by default."""
import hashlib
import hmac
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from .contract import PreparedCPE, interpret_nubefact_reply

_ALLOWED_HOSTS = {"api.nubefact.com", "demo.nubefact.com"}
_ROUTE = re.compile(r"^/api/v1/[A-Za-z0-9-]{10,100}/?$")
_MAX_REPLY = 1048576


class LiveEmissionDisabled(RuntimeError):
    pass


class SubmissionOutcomeUnknown(RuntimeError):
    """Could have reached provider. NEVER retry blindly; consult provider first."""
    pass


class ProviderIdentityMismatch(RuntimeError):
    pass


class _RejectRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class NubefactGateway:
    def __init__(self, *, route: str, token: str, enable_emission: bool = False, opener=None):
        parsed = urllib.parse.urlsplit(route)
        if (parsed.scheme != "https" or parsed.hostname not in _ALLOWED_HOSTS
                or parsed.port is not None or parsed.username or parsed.password
                or parsed.query or parsed.fragment or not _ROUTE.fullmatch(parsed.path)):
            raise ValueError("Invalid Nubefact route: HTTPS, approved host and API path required")
        if not isinstance(token, str) or not token.strip() or any(c.isspace() for c in token) or len(token) < 20:
            raise ValueError("Missing or invalid Nubefact API token")
        self.route = route
        self._token = token
        self.enable_emission = enable_emission
        self._opener = opener if opener is not None else urllib.request.build_opener(_RejectRedirect())

    def submit(self, prepared: PreparedCPE, *, human_authorized: bool = False) -> dict:
        if not self.enable_emission or not human_authorized:
            raise LiveEmissionDisabled("Requires explicit provider mode and an authorized send action")
        if not isinstance(prepared, PreparedCPE):
            raise ValueError("Only a prepared validated invoice may be submitted")
        if prepared.payload.get("operacion") != "generar_comprobante":
            raise ValueError("Unexpected operation")
        if prepared.payload.get("numero") != prepared.identity.number or prepared.payload.get("serie") != prepared.identity.series:
            raise ValueError("Document identity changed")
        # PreparedCPE.payload contains mutable dicts/lists although its dataclass is frozen.
        # Guard against modifications after validation; this is an integrity check,
        # NOT a signature or an authorization mechanism for untrusted objects.
        try:
            current_hash = hashlib.sha256(json.dumps(
                prepared.payload, sort_keys=True, separators=(",", ":"),
                ensure_ascii=False, allow_nan=False,
            ).encode("utf-8")).hexdigest()
        except (TypeError, ValueError, UnicodeError):
            raise ValueError("Prepared CPE contains unsupported payload data") from None
        if not isinstance(prepared.sha256, str) or not hmac.compare_digest(current_hash, prepared.sha256):
            raise ValueError("Prepared CPE changed after validation; prepare it again")
        if prepared.payload.get("tipo_de_comprobante") != (1 if prepared.identity.kind == "01" else 2):
            raise ValueError("Document type changed")
        request = urllib.request.Request(
            self.route,
            data=json.dumps(prepared.payload, ensure_ascii=False).encode("utf-8"),
            headers={"Authorization": f'Token token="{self._token}"',
                     "Content-Type": "application/json; charset=utf-8", "Accept": "application/json"},
            method="POST")
        try:
            with self._opener.open(request, timeout=20) as response:
                raw = response.read(_MAX_REPLY + 1)
                if len(raw) > _MAX_REPLY:
                    raise ValueError("Provider response exceeds size limit")
                parsed = json.loads(raw.decode("utf-8"))
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError, UnicodeError, ValueError):
            # Even for 4xx/5xx we cannot know remotely whether the document was processed.
            # No secret, URL, customer payload or server error text in exception.
            raise SubmissionOutcomeUnknown("Provider outcome uncertain; verify by identity before any retry") from None
        if not isinstance(parsed, dict):
            raise SubmissionOutcomeUnknown("Unexpected provider response; consult before retry")
        serie, number = parsed.get("serie"), parsed.get("numero")
        if serie is not None and serie != prepared.identity.series:
            raise ProviderIdentityMismatch("Provider returned a different series; manual review required")
        if number is not None and str(number) != str(prepared.identity.number):
            raise ProviderIdentityMismatch("Provider returned a different number; manual review required")
        # No auto-retry. Caller MUST persist normalized status and response atomically
        # with its own accounting outbox; Odoo integration is a separate gate.
        return interpret_nubefact_reply(parsed, prepared.identity)
