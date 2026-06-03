from fastapi import APIRouter,Depends,UploadFile,File,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.middlewave.auth_middleware import get_current_user
from app.schemas.document_schema import DocumentResponse
from app.services.document_service import save_uploaded_file
from app.models.document_model import Document
from app.utils.file_validator import validate_file
from app.services.audit_service import create_log
from celery.result import AsyncResult

router = APIRouter(
        prefix="/documents",
        tags=["Documents"]        
)

@router.get("/",response_model=list[DocumentResponse])
def get_documents(
        db:Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
        documents = db.query(Document).filter(Document.owner_id == current_user.id).all()
        return documents




@router.delete("/{document_id}")
def delete_document(
        document_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
        document = db.query(Document).filter(
                Document.id == document_id,
                Document.owner_id == current_user.id
        ).first()

        if not document:
                raise HTTPException(
                        status_code=404,
                        detail="Document not found"
                )

        create_log(
                db,
                current_user.id,
                "Document Delete"
        )

        db.delete(document)
        db.commit()

        return {
                "message": "Document deleted successfully"
        }


@router.post("/upload",response_model=DocumentResponse)
def upload_document(
        file: UploadFile = File(...),
        db:Session = Depends(get_db),
        current_user = Depends(get_current_user)
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
                current_user,
                db
        )
        return document

@router.get("/status/{task_id}")
def task_status(task_id: str):

    task = AsyncResult(task_id)

    return {
        "status": task.status
    }