from celery import Celery

celery = Celery("worker",broker="redis://localhost:6379/0",backend="redis://localhost:6379/0")

from celery.schedules import crontab
from app.services.tasks.migration_task import migrate_all_documents,migrate_documents_task



celery.conf.beat_schedule = {

    "sync-every-hour":
    {
        "task":
            "app.tasks.migration_tasks.incremental_sync",

        "schedule":
            crontab(
                minute=0
            )
    }
}

celery.conf.imports = (
        "from app.services.tasks.process_document_task",
        "from app.services.tasks.migration_task"
)