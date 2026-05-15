from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.user import User
from app.models.scan import Scan
from app.models.finding import Finding
from app.models.report import Report, ReportType
from app.auth.dependencies import get_current_user
from app.services.project_service import get_user_project
from app.ai.report_generator import generate_ai_report
from app.schemas.report import ReportCreate, ReportResponse

router = APIRouter(prefix="/projects/{project_id}/scans/{scan_id}/reports", tags=["reports"])


@router.post("/", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def create_report(
    project_id: UUID,
    scan_id: UUID,
    data: ReportCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_user_project(db, project_id, user)

    result = await db.execute(select(Scan).where(Scan.id == scan_id, Scan.project_id == project_id))
    scan = result.scalar_one_or_none()
    if not scan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan not found")

    findings_result = await db.execute(select(Finding).where(Finding.scan_id == scan_id))
    findings = findings_result.scalars().all()

    if not findings:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No findings to report — run the scan first")

    report_type = ReportType(data.report_type)
    ai_result = await generate_ai_report(scan.target_url, findings, report_type)

    report = Report(
        scan_id=scan_id,
        report_type=report_type,
        content=ai_result["content"],
        ai_summary=ai_result["summary"],
    )
    db.add(report)
    await db.flush()
    await db.refresh(report)
    return report


@router.get("/", response_model=list[ReportResponse])
async def list_reports(
    project_id: UUID,
    scan_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_user_project(db, project_id, user)
    result = await db.execute(
        select(Report).where(Report.scan_id == scan_id).order_by(Report.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    project_id: UUID,
    scan_id: UUID,
    report_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_user_project(db, project_id, user)
    result = await db.execute(select(Report).where(Report.id == report_id, Report.scan_id == scan_id))
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return report
