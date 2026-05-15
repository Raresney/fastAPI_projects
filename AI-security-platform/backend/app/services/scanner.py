import asyncio
from datetime import datetime
from uuid import UUID
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.finding import Finding, Severity
from app.models.scan import Scan, ScanStatus
from app.models.scan_log import ScanLog, LogLevel
from app.services.scan_modules import ALL_MODULES
from app.services.scan_modules.base import ScanResult
from app.websocket.manager import ws_manager


class ScannerService:
    def __init__(self, db: AsyncSession, scan_id: UUID):
        self.db = db
        self.scan_id = scan_id

    async def _log(self, message: str, level: LogLevel = LogLevel.INFO):
        log = ScanLog(scan_id=self.scan_id, message=message, level=level)
        self.db.add(log)
        await self.db.flush()
        await ws_manager.broadcast(str(self.scan_id), {
            "type": "scan_log",
            "level": level.value,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
        })

    async def _save_finding(self, result: ScanResult):
        finding = Finding(
            scan_id=self.scan_id,
            title=result.title,
            description=result.description,
            severity=Severity(result.severity),
            category=result.category,
            evidence=result.evidence,
            remediation=result.remediation,
        )
        self.db.add(finding)
        await self.db.flush()
        await ws_manager.broadcast(str(self.scan_id), {
            "type": "finding",
            "title": result.title,
            "severity": result.severity,
        })

    async def run(self, scan: Scan):
        scan.status = ScanStatus.RUNNING
        scan.started_at = datetime.utcnow()
        await self.db.flush()

        await ws_manager.broadcast(str(self.scan_id), {"type": "scan_started", "target": scan.target_url})
        await self._log(f"Scan started for {scan.target_url}")

        total_findings = 0

        async with httpx.AsyncClient(timeout=15.0, verify=False) as client:
            for module_cls in ALL_MODULES:
                module = module_cls()
                await self._log(f"Running module: {module.name}")

                try:
                    results = await module.run(scan.target_url, client)
                    for result in results:
                        await self._save_finding(result)
                        total_findings += 1
                    await self._log(f"Module {module.name} completed — {len(results)} finding(s)")
                except Exception as e:
                    await self._log(f"Module {module.name} failed: {str(e)}", LogLevel.ERROR)

        scan.status = ScanStatus.COMPLETED
        scan.completed_at = datetime.utcnow()
        await self.db.commit()

        await self._log(f"Scan completed — {total_findings} total finding(s)")
        await ws_manager.broadcast(str(self.scan_id), {
            "type": "scan_completed",
            "total_findings": total_findings,
        })
