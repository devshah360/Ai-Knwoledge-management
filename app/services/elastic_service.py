from elasticsearch import Elasticsearch

es = Elasticsearch("https://localhost:9200",basic_auth=("elastic", "DYPV55BW5vAwSYRVeVS="),verify_certs=False)

def index_document(document):

        data = {
                "filename": document.filename,
                "content":document.content,
                "owner_id":document.owner_id
        }

        es.index(
                index = "documents",
                id = document.id,
                document = data
        )

def search_documents(query):
        response = es.search(
                index = "documents",
                body = {
                        "query":{
                                "multi_match":{
                                "query":query,
                                "fields":[
                                        "filename",
                                        "content"
                                ]
                        }
                }
        }
)
        results = []

        for hit in response["hits"]["hits"]:
                results.append({
                        "id":hit["_id"],
                        "score":hit["_score"],
                        "data":hit["_source"],
                })

                return results