from fastapi import FastAPI

from backend.app.api.health import router as health_router
from backend.app.api.version import router as version_router

from backend.app.core.settings import settings
from backend.app.core.logging import logger

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

app.include_router(health_router)
app.include_router(version_router)


@app.on_event("startup")
async def startup():

    logger.info("Backend Started")


@app.on_event("shutdown")
async def shutdown():

    logger.info("Backend Stopped")
