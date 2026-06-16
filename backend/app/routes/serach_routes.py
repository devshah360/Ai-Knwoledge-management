from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.elastic_service import es
from app.services.elastic_service import search_documents
from app.models.search_model import SearchHistory
from app.services.search_analytics_service import save_search
from app.services.audit_service import create_log
from app.middlewave.auth_middleware import get_current_user

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.get("/")
def serach(
    query: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    response = es.search(
        index="documents",
        query={
            "multi_match": {
                "query": query,
                "fields": [
                    "filename",
                    "content"
                ]
            }
        },
        highlight={
            "fields": {
                "content": {}
            }
        }
    )

    results = []

    for hit in response["hits"]["hits"]:

        snippet = (
            hit.get("highlight",{})
            .get("content",
                 [hit["_source"]
                  ["content"][:200]]
                  )[0]
        )

        results.append({
            "id": hit["_id"],
            "title": hit["_source"]["filename"],
            "snippet": snippet,
            "score": hit["_score"]
        })

    save_search(db,query)

    create_log(
        db,
        current_user.id,
        f"Search: {query}"
    )
    return results


@router.get("/history")
def get_searches(
    db: Session = Depends(get_db)
):
    return (
        db.query(SearchHistory)
        .order_by(SearchHistory.id.desc())
        .all()
    )


@router.get("/health")
def health():

    return {
        "elastic_search": "running",
        "chroma": "running",
        "rag": "running"
    }

@router.get("/suggestions")
def suggestions(query: str):

    response = es.search(
        index="documents",
        query={
            "match_phrase_prefix":{
                "filename":query
                }
            },
            size=5
        )
    
    return [
        hit["_source"]["filename"]
        for hit in response["hits"]["hits"]
    ]


@router.get("/log")
def search_log(db:Session = Depends(get_db)):

    searches = (
        db.query(SearchHistory)
        .order_by(SearchHistory.id.desc())
        .limit(50)
        .all()
    )
    return [{
        "id": search.id,
        "query": search.query,
        "created_at": search.created_at
    }
    for search in searches
]