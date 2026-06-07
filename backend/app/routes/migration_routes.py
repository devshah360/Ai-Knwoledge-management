from fastapi import (
    APIRouter
)

from app.services.tasks.migration_task import (
    migrate_documents_task
)

router = APIRouter(
    prefix="/migration",
    tags=["Migration"]
)

@router.post("/start")
def start_migration():

    task = (
        migrate_documents_task
        .delay()
    )

    return {
        "task_id":
        task.id
    }
