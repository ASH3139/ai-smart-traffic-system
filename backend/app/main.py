from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.version import router as version_router

from app.core.settings import settings
from app.core.logging import logger

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