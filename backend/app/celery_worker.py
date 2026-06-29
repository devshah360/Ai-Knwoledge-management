from celery import Celery
from celery.schedules import crontab

celery = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.conf.imports = (
    "app.services.tasks.migration_task",
)

celery.conf.beat_schedule = {
    "sync-every-hour": {
        "task": "app.services.tasks.migration_task.incremental_sync",
        "schedule": crontab(minute=0),
    }
}