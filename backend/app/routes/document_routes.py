from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from celery.result import AsyncResult

from app.database import get_db
from app.middlewave.auth_middleware import get_current_user
from app.schemas.document_schema import DocumentResponse,RenameDocumentResponse
from app.services.document_service import save_uploaded_file
from app.services.elastic_service import remove_deleted_document
from app.services.vectorstore_service import delete_document_chunks
from app.services.audit_service import create_log
from app.models.document_model import Document
from app.utils.file_validator import validate_file
from app.celery_worker import celery
from app.services.notification_service import create_notification


from app.services.pdf_service import extract_text_from_pdf
from app.services.embedding_service import generate_embedding
from app.services.chunk_service import chunk_text
from app.services.vectorstore_service import delete_document_chunks,add_document_chunks
from app.services.elastic_service import remove_deleted_document,index_document

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.get("/", response_model=list[DocumentResponse])
def get_documents(
    db: Session = Depends(get_db),
    #current_user=Depends(get_current_user)
):
    documents = db.query(Document).filter(
    #    Document.owner_id == current_user.id
    ).all()

    return documents


@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    #current_user=Depends(get_current_user)
):
    try:
        content = file.file.read()

        validate_file(
            file.filename,
            len(content)
        )

        file.file.seek(0)

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    document = save_uploaded_file(
        file,
        db
       # current_user,
    )
    create_notification(
    f"Document Indexed: {file.filename}",
    "success"
)
    create_log(
        db,
       # current_user.id,
        f"Uploaded Document: {file.filename}"
    )

    return document


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
   # current_user=Depends(get_current_user)
):
    document = db.query(Document).filter(
        Document.id == document_id,
        #Document.owner_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    create_log(
        db,
       # current_user.id,
        f"Deleted Document: {document.filename}"
    )
    create_notification(
    f"Document Deleted: {document.filename}",
    "warning"
)
    delete_document_chunks(document_id)

    remove_deleted_document(document_id)

    db.delete(document)
    db.commit()

    return {
        "message": "Document deleted successfully"
    }


@router.put("/{document_id}")
def rename_document(
    document_id: int,
    data: RenameDocumentResponse,
    db: Session = Depends(get_db),
   # current_user=Depends(get_current_user)
):
    document = db.query(Document).filter(
        Document.id == document_id,
       # Document.owner_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    old_name = document.filename

    document.filename = data.filename

    db.commit()
    db.refresh(document)

    create_log(
        db,
       # current_user.id,
        f"Renamed Document: {old_name} -> {data.filename}"
    )

    return {
        "message": "Document renamed successfully",
        "document": {
            "id": document.id,
            "filename": document.filename
        }
    }


@router.post("/{document_id}/reindex")
def reindex_document(
    document_id: int,
    db: Session = Depends(get_db),
    #current_user=Depends(get_current_user)
):
    document = db.query(Document).filter(
        Document.id == document_id,
       # Document.owner_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    
    delete_document_chunks(document_id)
    remove_deleted_document(document_id)

    extracted_text = ""

    if document.filetype == "application/pdf":
        extracted_text = extract_text_from_pdf(document.filepath)
    elif document.filetype == "text/plain":
        with open(document.filepath,"r",encoding="utf-8") as f:
            extracted_text = f.read()

    if not extracted_text:
        raise HTTPException(
            status_code=400,
            detail="Unable to extract content"
        )
    
    embedding = generate_embedding(extracted_text[:1000])

    chunks = chunk_text(extracted_text)

    document.content = extracted_text
    document.embedding = embedding
    document.chunks = chunks

    add_document_chunks(document.id,chunks)

    index_document(document)

    create_log(
        db,
       # current_user.id,
        f"Reindexed Document: {document.filename}"
    )

    return {
        "message": "Document Re-index started successfully",
        "document_id": document.id,
        "chunks":len(chunks)
    }


@router.get("/status/{task_id}")
def task_status(task_id: str):
    task = AsyncResult(
        task_id,
        app=celery
    )

    return {
        "task_id": task_id,
        "status": task.status
    }