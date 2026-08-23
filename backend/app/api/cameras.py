from fastapi import APIRouter, Depends

from backend.app.database.session_manager import get_db_session
from backend.app.schemas.camera import CameraResponse
from backend.app.services.persistence.service import PersistenceService

router = APIRouter(
    prefix="/cameras",
    tags=["Cameras"],
)


persistence = PersistenceService()


@router.get(
    "",
    response_model=list[CameraResponse],
    summary="Get all cameras",
)
def get_cameras():
    """
    Returns all configured cameras.
    """

    with get_db_session() as session:

        return persistence.get_cameras(session)
