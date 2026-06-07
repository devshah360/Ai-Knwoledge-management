from app.celery_worker import celery
from app.services.chunk_service import chunk_text
from app.services.vectorstore_service import add_document_chunks
from app.services.embedding_service import generate_embedding

@celery.task
def process_document_tasks(document_id,text):
        chunks = chunk_text(text)

        add_document_chunks(document_id,chunks) 

        return {"status":"completed","chunk_created":len(chunks)}



@celery.task
def celery_task():
        print("Backround task working")
        return {"Success"}