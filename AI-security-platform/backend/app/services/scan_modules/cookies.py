import httpx
from app.services.scan_modules.base import BaseScanModule, ScanResult


class CookieSecurityModule(BaseScanModule):
    name = "cookies"
    category = "cookies"

    async def run(self, target_url: str, client: httpx.AsyncClient) -> list[ScanResult]:
        results = []
        resp = await client.get(target_url, follow_redirects=True)

        for cookie in resp.cookies.jar:
            flags = []
            if not cookie.secure:
                flags.append("Secure")
            if "httponly" not in str(cookie).lower():
                flags.append("HttpOnly")
            if "samesite" not in str(cookie).lower():
                flags.append("SameSite")

            if flags:
                results.append(ScanResult(
                    title=f"Cookie '{cookie.name}' missing security flags",
                    description=f"Cookie is missing: {', '.join(flags)}",
                    severity="medium" if "Secure" in flags or "HttpOnly" in flags else "low",
                    category=self.category,
                    evidence=f"Set-Cookie: {cookie.name}=...; flags present: {str(cookie)}",
                    remediation=f"Add {', '.join(flags)} flags to the {cookie.name} cookie",
                ))

        return results
