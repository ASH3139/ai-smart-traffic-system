from fastapi import FastAPI

from backend.app.api.health import router as health_router
from backend.app.api.version import router as version_router
from backend.app.core.settings import settings
from backend.app.core.logging import logger
from backend.app.dependencies.system import system
from backend.app.api.analytics import router as analytics_router
from backend.app.api.lanes import router as lanes_router
from backend.app.api.signal import router as signal_router
from backend.app.api.video import router as video_router
from backend.app.system import system
from backend.app.api.statistics import router as statistics_router
from backend.app.api.decision import router as decision_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)


app.include_router(health_router)
app.include_router(version_router)
app.include_router(analytics_router)
app.include_router(lanes_router)
app.include_router(signal_router)
app.include_router(video_router)
app.include_router(statistics_router)
app.include_router(decision_router)


@app.on_event("startup")
async def startup():

    system.start()

    logger.info("Backend Started")


@app.on_event("shutdown")
async def shutdown():

    system.stop()

    logger.info("Backend Stopped")
