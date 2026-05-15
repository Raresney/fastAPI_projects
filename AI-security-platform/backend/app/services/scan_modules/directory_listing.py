from urllib.parse import urljoin
import httpx
from app.services.scan_modules.base import BaseScanModule, ScanResult

COMMON_DIRS = ["/", "/images/", "/css/", "/js/", "/assets/", "/uploads/", "/static/", "/media/", "/files/", "/backup/"]
LISTING_INDICATORS = ["index of", "directory listing", "<pre>", "parent directory"]


class DirectoryListingModule(BaseScanModule):
    name = "directory_listing"
    category = "information_disclosure"

    async def run(self, target_url: str, client: httpx.AsyncClient) -> list[ScanResult]:
        results = []

        for directory in COMMON_DIRS:
            url = urljoin(target_url, directory)

            try:
                resp = await client.get(url, follow_redirects=True)
                if resp.status_code == 200:
                    body = resp.text.lower()
                    if any(indicator in body for indicator in LISTING_INDICATORS):
                        results.append(ScanResult(
                            title=f"Directory listing enabled at {directory}",
                            description=f"Directory listing is enabled, exposing file structure at {directory}",
                            severity="medium",
                            category=self.category,
                            evidence=f"GET {url} contains directory listing indicators",
                            remediation="Disable directory listing in your web server configuration",
                        ))
            except httpx.HTTPError:
                continue

        return results
