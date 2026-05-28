from fastapi import APIRouter,Depends
from app.middlewave.auth_middleware import get_current_user
from app.services.elastic_service import search_documents

router = APIRouter(
        prefix="/search",
        tags=["Search"]
)

@router.get("/")
def serach(
        query:str,
        current_user = Depends(get_current_user)
):
        results = search_documents(query)

        return results