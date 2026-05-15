import asyncio
import httpx
from app.services.scan_modules.base import BaseScanModule, ScanResult


class RateLimitingModule(BaseScanModule):
    name = "rate_limiting"
    category = "rate_limiting"

    async def run(self, target_url: str, client: httpx.AsyncClient) -> list[ScanResult]:
        results = []
        blocked = False

        tasks = [client.get(target_url, follow_redirects=True) for _ in range(20)]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for resp in responses:
            if isinstance(resp, httpx.Response) and resp.status_code == 429:
                blocked = True
                break

        if not blocked:
            has_rate_headers = False
            for resp in responses:
                if isinstance(resp, httpx.Response):
                    rate_headers = {k for k in resp.headers if "ratelimit" in k.lower() or "x-rate" in k.lower()}
                    if rate_headers:
                        has_rate_headers = True
                        break

            if not has_rate_headers:
                results.append(ScanResult(
                    title="No rate limiting detected",
                    description="Server did not return 429 or rate-limit headers after 20 rapid requests",
                    severity="medium",
                    category=self.category,
                    evidence="20 rapid GET requests all returned 2xx with no rate-limit headers",
                    remediation="Implement rate limiting (e.g., token bucket, sliding window) to prevent brute-force and DoS",
                ))

        return results
