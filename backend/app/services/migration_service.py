from elasticsearch import helpers

from app.services.elastic_service import (
    es
)
from app.services.mssql_service import (
    fetch_documents
)

def bulk_index(
    documents
):

    actions = []

    for doc in documents:

        actions.append(
            {
                "_index":
                    "documents",

                "_id":
                    doc["id"],

                "_source":
                {
                    "title":
                        doc["title"],

                    "content":
                        doc["content"],

                    "updated_at":
                        str(
                            doc[
                                "updated_at"
                            ]
                        )
                }
            }
        )

    helpers.bulk(
        es,
        actions
    )

def migrate_all_documents():

    docs = fetch_documents()

    bulk_index(
        docs
    )

    return {
        "migrated":
        len(docs)
    }