from urllib.parse import urlencode
import httpx
from app.services.scan_modules.base import BaseScanModule, ScanResult

REDIRECT_PARAMS = ["url", "redirect", "next", "return", "returnTo", "redirect_uri", "continue", "dest", "destination", "go", "target"]


class OpenRedirectModule(BaseScanModule):
    name = "open_redirect"
    category = "redirect"

    async def run(self, target_url: str, client: httpx.AsyncClient) -> list[ScanResult]:
        results = []
        evil_url = "https://evil-attacker.com"

        for param in REDIRECT_PARAMS:
            test_url = f"{target_url}?{urlencode({param: evil_url})}"

            try:
                resp = await client.get(test_url, follow_redirects=False)

                if resp.status_code in (301, 302, 303, 307, 308):
                    location = resp.headers.get("Location", "")
                    if evil_url in location:
                        results.append(ScanResult(
                            title=f"Open redirect via '{param}' parameter",
                            description=f"Server redirects to attacker-controlled URL when '{param}' parameter is set",
                            severity="medium",
                            category=self.category,
                            evidence=f"GET {test_url} → {resp.status_code} Location: {location}",
                            remediation=f"Validate the '{param}' parameter against an allowlist of trusted domains",
                        ))
                        break
            except httpx.HTTPError:
                continue

        return results
