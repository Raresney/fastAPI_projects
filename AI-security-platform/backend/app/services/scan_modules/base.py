from abc import ABC, abstractmethod
from dataclasses import dataclass
import httpx


@dataclass
class ScanResult:
    title: str
    description: str
    severity: str
    category: str
    evidence: str | None = None
    remediation: str | None = None


class BaseScanModule(ABC):
    name: str = "base"
    category: str = "general"

    @abstractmethod
    async def run(self, target_url: str, client: httpx.AsyncClient) -> list[ScanResult]:
        pass
