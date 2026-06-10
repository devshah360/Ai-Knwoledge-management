from app.celery_worker import celery

from app.services.migration_service import (
    migrate_all_documents
)

from app.services.notification_service import (
    create_notification
)


@celery.task
def migrate_documents_task():

    result = migrate_all_documents()

    create_notification(
        "Migration completed",
        "success"
    )

    return result