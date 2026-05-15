from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models.user import User
from app.models.scan import Scan
from app.models.finding import Finding
from app.auth.dependencies import get_current_user
from app.services.project_service import get_user_project
from app.services.scanner import ScannerService
from app.schemas.scan import ScanCreate, ScanResponse
from app.schemas.finding import FindingResponse

router = APIRouter(prefix="/projects/{project_id}/scans", tags=["scans"])


@router.post("/", response_model=ScanResponse, status_code=status.HTTP_201_CREATED)
async def create_scan(
    project_id: UUID,
    data: ScanCreate,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    project = await get_user_project(db, project_id, user)

    scan = Scan(project_id=project.id, target_url=str(data.target_url))
    db.add(scan)
    await db.flush()
    await db.refresh(scan)

    return scan


@router.get("/", response_model=list[ScanResponse])
async def list_scans(
    project_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_user_project(db, project_id, user)
    result = await db.execute(
        select(Scan).where(Scan.project_id == project_id).order_by(Scan.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{scan_id}", response_model=ScanResponse)
async def get_scan(
    project_id: UUID,
    scan_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_user_project(db, project_id, user)
    result = await db.execute(select(Scan).where(Scan.id == scan_id, Scan.project_id == project_id))
    scan = result.scalar_one_or_none()
    if not scan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan not found")
    return scan


@router.get("/{scan_id}/findings", response_model=list[FindingResponse])
async def get_findings(
    project_id: UUID,
    scan_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_user_project(db, project_id, user)
    result = await db.execute(
        select(Finding).where(Finding.scan_id == scan_id).order_by(Finding.created_at)
    )
    return result.scalars().all()


@router.post("/{scan_id}/run", response_model=dict)
async def run_scan(
    project_id: UUID,
    scan_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_user_project(db, project_id, user)
    result = await db.execute(select(Scan).where(Scan.id == scan_id, Scan.project_id == project_id))
    scan = result.scalar_one_or_none()
    if not scan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan not found")

    scanner = ScannerService(db, scan.id)
    await scanner.run(scan)

    return {"status": "completed", "scan_id": str(scan.id)}
