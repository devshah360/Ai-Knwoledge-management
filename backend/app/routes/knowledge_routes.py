from fastapi import APIRouter
from app.services.agents.extract_agent import extract_key_points
from app.services.agents.comparsion_agent import compare_document

router = APIRouter(
        prefix="/knowledge",
        tags=["Knowledge"]
)

@router.post("/extract")
def extract(text:str):
        return {
                "result":extract_key_points(text)
        }

@router.post("/compare")
def compare(doc1:str,doc2:str):
        
        result = compare_document(doc1,doc2)

        return {
                "comparsion":result
        }

