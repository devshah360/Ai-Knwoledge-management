from fastapi import APIRouter

router = APIRouter(
        prefix="/system",
        tags=["System"]
)

@router.get("/health")
def health():
        return {
                "status":"healthy"
        }

@router.get("/database")
def database_health():
        return {
                "postgre":"running",
                "mongo":"running",
                "elastic":"running",
                "redis":"running"
        }

