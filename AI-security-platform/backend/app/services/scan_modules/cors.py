import httpx
from app.services.scan_modules.base import BaseScanModule, ScanResult


class CORSModule(BaseScanModule):
    name = "cors"
    category = "cors"

    async def run(self, target_url: str, client: httpx.AsyncClient) -> list[ScanResult]:
        results = []
        evil_origin = "https://evil-attacker.com"

        resp = await client.get(
            target_url,
            headers={"Origin": evil_origin},
            follow_redirects=True,
        )

        acao = resp.headers.get("Access-Control-Allow-Origin", "")

        if acao == "*":
            results.append(ScanResult(
                title="CORS wildcard origin",
                description="Access-Control-Allow-Origin is set to * — any domain can make cross-origin requests",
                severity="medium",
                category=self.category,
                evidence=f"Access-Control-Allow-Origin: {acao}",
                remediation="Restrict CORS to specific trusted origins",
            ))
        elif evil_origin in acao:
            results.append(ScanResult(
                title="CORS origin reflection",
                description="Server reflects arbitrary Origin header in ACAO — attacker-controlled origins are trusted",
                severity="high",
                category=self.category,
                evidence=f"Sent Origin: {evil_origin}, Got ACAO: {acao}",
                remediation="Validate Origin against an allowlist instead of reflecting it",
            ))

        if resp.headers.get("Access-Control-Allow-Credentials", "").lower() == "true" and acao != "":
            results.append(ScanResult(
                title="CORS credentials allowed with permissive origin",
                description="Credentials are allowed with a permissive ACAO — cookies and auth headers can be stolen cross-origin",
                severity="high",
                category=self.category,
                evidence=f"ACAO: {acao}, Access-Control-Allow-Credentials: true",
                remediation="Never combine Allow-Credentials: true with wildcard or reflected origins",
            ))

        return results
