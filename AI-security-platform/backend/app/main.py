from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database.session import engine, Base
from app.utils.logging import setup_logging
from app.utils.rate_limiter import rate_limiter
from app.routers import auth, users, projects, scans, reports, ws

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(settings.DEBUG)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1", dependencies=[Depends(rate_limiter)])
app.include_router(users.router, prefix="/api/v1", dependencies=[Depends(rate_limiter)])
app.include_router(projects.router, prefix="/api/v1", dependencies=[Depends(rate_limiter)])
app.include_router(scans.router, prefix="/api/v1", dependencies=[Depends(rate_limiter)])
app.include_router(reports.router, prefix="/api/v1", dependencies=[Depends(rate_limiter)])
app.include_router(ws.router)


@app.get("/")
def health():
    return {"status": "running", "service": settings.APP_NAME}
