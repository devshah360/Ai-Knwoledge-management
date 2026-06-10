from celery import chunks
from langchain_ollama import OllamaLLM
from opentelemetry import context
from app.core.config import OLLAMA_URL
from app.services.search_service import hybrid_search
from app.services.search_analytics_service import save_search
from app.services.memory_service import (
    memory_to_text,
    get_recent_memory
)
from app.models.chat_model import ChatHistory
from app.services.mongo_service import (
    create_conversation,
    add_message
)

llm = OllamaLLM(
    model = "qwen2.5:3b",
    base_url=OLLAMA_URL
)

def rag_chat(question,db,top_k=3):

    print("start")

    results = hybrid_search(question)

    print("ELASTIC COUNT:", len(results["elastic_results"]))
    print("VECTOR COUNT:", len(results["vector_results"]))
    
    seen = set()
    chunks = []
    text = ""

    for item in results["elastic_results"]:
        text = item["_source"]["content"]

        print("ELASTIC TEXT FOUND:", text[:100])
        
        if text not in seen:
            seen.add(text)
            chunks.append(text)

    for doc in results["vector_results"]:
        text = doc.page_content

        print("VECTOR TEXT FOUND:", text[:100])

        if text not in seen:
            seen.add(text)
            chunks.append(text)

    context = "\n".join(chunks)

    print("CHUNKS COUNT:", len(chunks))
    print("CONTEXT:")
    print(context)

    if not context.strip():
        return {
            "answer": "No relevant information found.",
            "context": ""
    }

    prompt = f"""
    You are a RAG assistant.

    Answer ONLY from the provided context.

    If the answer cannot be found in the context, say:
    "I could not find this information in the provided documents."

    Context:
    {context}

    Question:
    {question}
    """

    answer = llm.invoke(prompt)

    conversation_id = create_conversation(
    title=question[:50]
)

    add_message(
        conversation_id,
        "user",
        question
    )

    add_message(
        conversation_id,
        "assistant",
        answer
    )

    save_search(
        db,
        question
    )

    chat = ChatHistory(
        question=question,
        answer=answer,
        sources="RAG",
    )

    print("reached")

    db.add(chat)
    db.commit()

    print("store")

    return {
    "conversation_id": conversation_id,
    "answer": answer,
    "context": context
}