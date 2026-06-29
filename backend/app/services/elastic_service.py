from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

es = Elasticsearch("https://localhost:9200",basic_auth=("elastic", "Devshah@1"),verify_certs=False)

INDEX_NAME = "documents"


def create_index_if_not_exists():
    """
    Create Elasticsearch index if it does not exist.
    """
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(
            index=INDEX_NAME,
            mappings={
                "properties": {
                    "filename": {"type": "text"},
                    "content": {"type": "text"},
                    "owner_id": {"type": "integer"}
                }
            }
        )
        print(f"Index '{INDEX_NAME}' created")


# Create index on startup
create_index_if_not_exists()


def index_document(document):

    data = {
        "filename": document.filename,
        "content": document.content,
        "owner_id": document.owner_id
    }

    print("=" * 50)
    print("INDEXING DOCUMENT")
    print("ID:", document.id)
    print("Filename:", document.filename)
    print("Content Length:", len(document.content))
    print("=" * 50)

    response = es.index(
        index=INDEX_NAME,
        id=document.id,
        document=data,
        refresh=True
    )

    print(response)

    return response


def search_documents(query):
    """
    Search documents by filename and content.
    """

    try:
        response = es.search(
            index=INDEX_NAME,
            query={
                "multi_match": {
                    "query": query,
                    "fields": [
                        "filename",
                        "content"
                    ]
                }
            }
        )

        results = []

        for hit in response["hits"]["hits"]:
            results.append({
                "id": hit["_id"],
                "score": hit["_score"],
                "data": hit["_source"]
            })

        return results

    except NotFoundError:
        create_index_if_not_exists()
        return []


def remove_deleted_document(document_id):
    """
    Delete document from Elasticsearch.
    """

    try:
        es.delete(
            index=INDEX_NAME,
            id=document_id,
            refresh=True
        )

    except NotFoundError:
        pass