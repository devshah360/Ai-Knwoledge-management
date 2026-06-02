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
        return retrieve_chunks(query,top_k=5)

def hybrid_search(query:str):
        elastic_results = elastic_search(query)
        vector_results = semantic_search(query)

        return{
                "elastic_results":elastic_results,
                "vector_results":vector_results
        }