import asyncio
from uuid import UUID
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from app.tasks.celery_app import celery_app
from app.config import get_settings
from app.models.scan import Scan, ScanStatus
from app.models.finding import Finding, Severity
from app.services.scan_modules import ALL_MODULES
from app.services.scan_modules.base import ScanResult
from datetime import datetime
import httpx

settings = get_settings()
sync_engine = create_engine(settings.DATABASE_URL_SYNC)


def _run_modules_sync(target_url: str) -> list[ScanResult]:
    async def _run():
        all_results = []
        async with httpx.AsyncClient(timeout=15.0, verify=False) as client:
            for module_cls in ALL_MODULES:
                module = module_cls()
                try:
                    results = await module.run(target_url, client)
                    all_results.extend(results)
                except Exception:
                    pass
        return all_results
    return asyncio.run(_run())


@celery_app.task(bind=True, max_retries=3)
def run_scan_task(self, scan_id: str):
    with Session(sync_engine) as db:
        scan = db.execute(select(Scan).where(Scan.id == UUID(scan_id))).scalar_one()
        scan.status = ScanStatus.RUNNING
        scan.started_at = datetime.utcnow()
        db.commit()

        try:
            results = _run_modules_sync(scan.target_url)

            for r in results:
                finding = Finding(
                    scan_id=scan.id,
                    title=r.title,
                    description=r.description,
                    severity=Severity(r.severity),
                    category=r.category,
                    evidence=r.evidence,
                    remediation=r.remediation,
                )
                db.add(finding)

            scan.status = ScanStatus.COMPLETED
            scan.completed_at = datetime.utcnow()
            db.commit()
        except Exception as exc:
            scan.status = ScanStatus.FAILED
            db.commit()
            raise self.retry(exc=exc, countdown=30)
