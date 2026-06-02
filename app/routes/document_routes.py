from fastapi import APIRouter,Depends,UploadFile,File,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.middlewave.auth_middleware import get_current_user
from app.schemas.document_schema import DocumentResponse
from app.services.document_service import save_uploaded_file
from app.models.document_model import Document

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

@router.get("/{document_id}")
def get_document(
        document_id: int,
        db:Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
        document = db.query(Document).filter(
                Document.id == document_id,
                Document.owner_id == current_user.id).first()
        
        if not document:
                raise HTTPException(
                        status_code=404,
                        detail="document not found"
                )
        return document


@router.post("/upload",response_model=DocumentResponse)
def upload_document(
        file: UploadFile = File(...),
        db:Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
        allowed_types = [
                "application/pdf",
                "text/plain"
        ]

        if file.content_type not in allowed_types:
                raise HTTPException(
                        status_code=400,
                        detail="Invalid File Type"
                )
        MAX_SIZE = 5*1024*1024
        
        document = save_uploaded_file(
                file,
                current_user,
                db
        )
        return document