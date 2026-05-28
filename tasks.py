from celery_worker import celery

@celery.task
def celery_task():
        print("Backround task working")
        return {"Success"}