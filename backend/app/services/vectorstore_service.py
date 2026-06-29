from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = Chroma(
    collection_name="documents",
    embedding_function=embedding_model,
    persist_directory="./chroma_db"
)


def add_document_chunks(document_id, chunks):

    ids = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        ids.append(f"{document_id}_{index}")

        metadatas.append({
            "document_id": str(document_id),
            "chunk_id": index
        })

    vector_store.add_texts(
        texts=chunks,
        ids=ids,
        metadatas=metadatas
    )

    print("Inserted into Chroma:", len(chunks))


def retrieve_chunks(query, top_k=8):

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": top_k,
            "fetch_k": 20
        }
    )

    docs = retriever.invoke(query)

    print("Retrieved Chunks:", len(docs))

    for i, doc in enumerate(docs):

        print(f"\n------ CHUNK {i+1} ------")
        print(doc.page_content[:300])

    return docs


def delete_document_chunks(document_id):

    vector_store.delete(
        where={
            "document_id": str(document_id)
        }
    )