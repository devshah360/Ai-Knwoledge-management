from app.services.elastic_service import es
from app.services.vectorstore_service import retrieve_chunks


def elastic_search(query: str, top_k=3):

    result = es.search(
        index="documents",
        size=top_k,
        body={
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": [
                        "content",
                        "filename"
                    ]
                }
            }
        }
    )

    return result["hits"]["hits"]


def semantic_search(query: str, top_k=3):

    return retrieve_chunks(
        query=query,
        top_k=top_k
    )


def hybrid_search(query: str, top_k=3):

    elastic_results = elastic_search(
        query=query,
        top_k=top_k
    )

    vector_results = semantic_search(
        query=query,
        top_k=top_k
    )

    print("ELASTIC RESULTS:", len(elastic_results))
    print("VECTOR RESULTS:", len(vector_results))

    return {
        "elastic_results": elastic_results,
        "vector_results": vector_results
    }