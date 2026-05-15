import asyncio
from uuid import UUID
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from app.tasks.celery_app import celery_app
from app.config import get_settings
from app.models.scan import Scan
from app.models.finding import Finding
from app.models.report import Report, ReportType
from app.ai.report_generator import generate_ai_report

settings = get_settings()
sync_engine = create_engine(settings.DATABASE_URL_SYNC)


@celery_app.task(bind=True, max_retries=2)
def generate_report_task(self, scan_id: str, report_type: str = "executive"):
    with Session(sync_engine) as db:
        scan = db.execute(select(Scan).where(Scan.id == UUID(scan_id))).scalar_one()
        findings = db.execute(select(Finding).where(Finding.scan_id == scan.id)).scalars().all()

        if not findings:
            return {"error": "No findings"}

        rt = ReportType(report_type)
        ai_result = asyncio.run(generate_ai_report(scan.target_url, findings, rt))

        report = Report(
            scan_id=scan.id,
            report_type=rt,
            content=ai_result["content"],
            ai_summary=ai_result["summary"],
        )
        db.add(report)
        db.commit()

        return {"report_id": str(report.id)}
