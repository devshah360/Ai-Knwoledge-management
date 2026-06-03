from app.services.elastic_service import es
from app.services.vectorstore_service import retrieve_chunks

def elastic_search(query:str):
        result = es.search(
                index="documents",
                body={
                        "query":{
                                "multi_match":{
                                        "query":query,
                                        "fields":[
                                                "content",
                                                "filename"
                                        ]
                                }
                        }
                }
        )
        return result["hits"]["hits"]

def semantic_search(query:str):
        return retrieve_chunks(query,top_k=3)

def hybrid_search(query: str):

    elastic_results = elastic_search(query)
    vector_results = semantic_search(query)

    results = []

    for item in elastic_results:
        item["source"] = "elastic"
        results.append(item)

    for item in vector_results:
        item["source"] = "semantic"
        results.append(item)

    ranked_results = sorted(
        results,
        key=lambda x: x.get("score", 0),
        reverse=True
    )

    return ranked_results