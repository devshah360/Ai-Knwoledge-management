from fastapi import APIRouter

router = APIRouter(
    prefix="/monitoring",
    tags=["Monitoring"]
)
@router.get("/status")
def status():

    return {
        "api":"running",
        "elastic":"running",
        "mongo":"running",
        "redis":"running"
    }