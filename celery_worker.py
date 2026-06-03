from celery import Celery

celery = Celery("worker",broker="redis://localhost:6379/0",backend="redis://localhost:6379/0")

from celery.schedules import (
    crontab
)

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