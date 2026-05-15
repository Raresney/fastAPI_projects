import httpx
from app.services.scan_modules.base import BaseScanModule, ScanResult

DANGEROUS_METHODS = ["PUT", "DELETE", "TRACE", "CONNECT"]


class HTTPMethodsModule(BaseScanModule):
    name = "http_methods"
    category = "methods"

    async def run(self, target_url: str, client: httpx.AsyncClient) -> list[ScanResult]:
        results = []

        try:
            resp = await client.request("OPTIONS", target_url, follow_redirects=True)
            allow = resp.headers.get("Allow", "")

            for method in DANGEROUS_METHODS:
                if method in allow.upper():
                    results.append(ScanResult(
                        title=f"Dangerous HTTP method enabled: {method}",
                        description=f"{method} method is allowed on the server",
                        severity="medium" if method == "TRACE" else "low",
                        category=self.category,
                        evidence=f"Allow: {allow}",
                        remediation=f"Disable {method} method if not required",
                    ))
        except httpx.HTTPError:
            pass

        try:
            resp = await client.request("TRACE", target_url, follow_redirects=False)
            if resp.status_code == 200:
                results.append(ScanResult(
                    title="TRACE method enabled — XST risk",
                    description="TRACE method responds with 200, enabling Cross-Site Tracing attacks",
                    severity="medium",
                    category=self.category,
                    evidence=f"TRACE {target_url} returned {resp.status_code}",
                    remediation="Disable the TRACE HTTP method on the web server",
                ))
        except httpx.HTTPError:
            pass

        return results
