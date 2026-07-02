from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers.scan import router as scan_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["System"])
async def root():
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }


@app.get("/health", tags=["System"])
async def health():
    return {
        "status": "healthy"
    }


app.include_router(
    scan_router,
    prefix="/api/v1/scan",
    tags=["Network Scan"]
)