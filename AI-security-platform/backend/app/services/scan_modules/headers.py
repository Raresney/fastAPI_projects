import httpx
from app.services.scan_modules.base import BaseScanModule, ScanResult

SECURITY_HEADERS = {
    "Strict-Transport-Security": {
        "severity": "high",
        "desc": "HSTS header missing — vulnerable to protocol downgrade attacks",
        "fix": "Add Strict-Transport-Security: max-age=31536000; includeSubDomains",
    },
    "X-Content-Type-Options": {
        "severity": "medium",
        "desc": "X-Content-Type-Options missing — browser may MIME-sniff responses",
        "fix": "Add X-Content-Type-Options: nosniff",
    },
    "X-Frame-Options": {
        "severity": "medium",
        "desc": "X-Frame-Options missing — page can be embedded in iframes (clickjacking)",
        "fix": "Add X-Frame-Options: DENY or SAMEORIGIN",
    },
    "Content-Security-Policy": {
        "severity": "high",
        "desc": "CSP header missing — no protection against XSS and data injection",
        "fix": "Implement a Content-Security-Policy with restrictive directives",
    },
    "X-XSS-Protection": {
        "severity": "low",
        "desc": "X-XSS-Protection header missing",
        "fix": "Add X-XSS-Protection: 1; mode=block (legacy browsers)",
    },
    "Referrer-Policy": {
        "severity": "low",
        "desc": "Referrer-Policy missing — referrer information may leak to third parties",
        "fix": "Add Referrer-Policy: strict-origin-when-cross-origin",
    },
    "Permissions-Policy": {
        "severity": "low",
        "desc": "Permissions-Policy missing — browser features not explicitly restricted",
        "fix": "Add Permissions-Policy to restrict camera, microphone, geolocation, etc.",
    },
}


class SecurityHeadersModule(BaseScanModule):
    name = "security_headers"
    category = "headers"

    async def run(self, target_url: str, client: httpx.AsyncClient) -> list[ScanResult]:
        results = []
        resp = await client.get(target_url, follow_redirects=True)

        for header, info in SECURITY_HEADERS.items():
            if header.lower() not in {k.lower() for k in resp.headers.keys()}:
                results.append(ScanResult(
                    title=f"Missing {header}",
                    description=info["desc"],
                    severity=info["severity"],
                    category=self.category,
                    evidence=f"Response headers: {dict(resp.headers)}",
                    remediation=info["fix"],
                ))

        server = resp.headers.get("Server")
        if server:
            results.append(ScanResult(
                title="Server version disclosed",
                description=f"Server header exposes: {server}",
                severity="info",
                category=self.category,
                evidence=f"Server: {server}",
                remediation="Remove or obfuscate the Server header",
            ))

        x_powered = resp.headers.get("X-Powered-By")
        if x_powered:
            results.append(ScanResult(
                title="Technology stack disclosed",
                description=f"X-Powered-By header exposes: {x_powered}",
                severity="low",
                category=self.category,
                evidence=f"X-Powered-By: {x_powered}",
                remediation="Remove the X-Powered-By header",
            ))

        return results
