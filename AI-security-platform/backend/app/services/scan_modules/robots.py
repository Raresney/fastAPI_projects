from urllib.parse import urljoin
import httpx
from app.services.scan_modules.base import BaseScanModule, ScanResult

SENSITIVE_PATTERNS = ["/admin", "/backup", "/config", "/database", "/api", "/private", "/secret", "/wp-admin", "/phpmyadmin", "/.env", "/.git"]


class RobotsModule(BaseScanModule):
    name = "robots"
    category = "information_disclosure"

    async def run(self, target_url: str, client: httpx.AsyncClient) -> list[ScanResult]:
        results = []
        robots_url = urljoin(target_url, "/robots.txt")

        resp = await client.get(robots_url, follow_redirects=True)

        if resp.status_code == 200 and len(resp.text) > 0:
            body = resp.text.lower()

            sensitive_found = [p for p in SENSITIVE_PATTERNS if p.lower() in body]
            if sensitive_found:
                results.append(ScanResult(
                    title="robots.txt exposes sensitive paths",
                    description=f"robots.txt reveals potentially sensitive directories: {', '.join(sensitive_found)}",
                    severity="medium",
                    category=self.category,
                    evidence=resp.text[:1000],
                    remediation="Review robots.txt — avoid listing internal paths that help attackers map the application",
                ))
            else:
                results.append(ScanResult(
                    title="robots.txt is publicly accessible",
                    description="robots.txt file exists and is readable",
                    severity="info",
                    category=self.category,
                    evidence=resp.text[:500],
                    remediation="Ensure robots.txt does not reveal sensitive application structure",
                ))

        return results
