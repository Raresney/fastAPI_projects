import time
from collections import defaultdict
from fastapi import Request, HTTPException, status


class RateLimiter:
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)

    def _cleanup(self, key: str):
        now = time.time()
        self._requests[key] = [t for t in self._requests[key] if now - t < self.window]

    async def __call__(self, request: Request):
        client_ip = request.client.host if request.client else "unknown"
        self._cleanup(client_ip)

        if len(self._requests[client_ip]) >= self.max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
            )

        self._requests[client_ip].append(time.time())


rate_limiter = RateLimiter()
