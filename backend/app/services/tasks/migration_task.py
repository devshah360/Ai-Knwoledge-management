from app.celery_worker import celery

from app.services.migration_service import (
    migrate_all_documents
)
@celery.task
def migrate_documents_task():

    return (
        migrate_all_documents()
    )