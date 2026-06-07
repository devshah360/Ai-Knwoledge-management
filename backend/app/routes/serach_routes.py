from fastapi import APIRouter,Depends
from app.middlewave.auth_middleware import get_current_user
from app.services.elastic_service import search_documents
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.search_model import SearchHistory
from app.services.search_analytics_service import save_search
router = APIRouter(
        prefix="/search",
        tags=["Search"]
)

@router.get("/")
def serach(
        query:str,
        db:Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
        results = search_documents(query)

        save_search(db,query)
        
        return results

@router.get("/history")
def get_searches(db:Session = Depends(get_db)):
        return (db.query(SearchHistory).order_by(SearchHistory.id.desc()).all())

@router.get("/health")
def health():

        return {
                "elastic_search":"running",
                "chroma":"running",
                "rag":"running"
        }