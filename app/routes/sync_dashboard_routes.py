from fastapi import APIRouter

router = APIRouter(
    prefix="/sync-dashboard",
    tags=["Sync Dashboard"]
)

@router.get("/stats")
def migration_stats():

    return {

        "last_sync":
            "...",

        "documents":
            15000,

        "status":
            "healthy"
    }