from app.services.vectorstore_service import retrieve_chunks

def search_agent(query):
        docs = retrieve_chunks(query,top_k=3)
        context = "\n\n".join([
                doc.page_content
                for doc in docs
        ])

        return {
                "context":context,
                "document_found":len(docs)
        }
#Question->Retriver->Relative Context 