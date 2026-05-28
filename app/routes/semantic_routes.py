from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.document_model import Document
from app.middlewave.auth_middleware import get_current_user
from app.services.embedding_service import generate_embedding
from app.services.vector_service import cosine_similarity

router = APIRouter(
        prefix="/semantic-search",
        tags = ["Semantic Search"]
)

@router.get("/")
def semantic_search(query:str,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
        query_embedding = generate_embedding(query)

        documents = db.query(Document).filter(Document.owner_id == current_user.id).all()

        results = []

        for doc in documents:
                if doc.embedding:
                        similarity = cosine_similarity(query_embedding,doc.embedding)
                        results.append({
                                "document_id":doc.id,
                                "filename":doc.filename,
                                "similarity":float(similarity)
                        })

                        results.sort(key=lambda x:x["similarity"],reverse=True)

                        return results[:5]