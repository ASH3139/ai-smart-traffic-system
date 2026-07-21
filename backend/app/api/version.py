from fastapi import APIRouter

router = APIRouter()


@router.get("/version")
def version():
    return {
        "project": "AI Smart Traffic System",
        "version": "1.0.0"
    }