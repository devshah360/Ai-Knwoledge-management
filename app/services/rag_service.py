from langchain_ollama import OllamaLLM
from app.core.config import OLLAMA_URL
from app.services.search_service import hybrid_search
from app.services.search_analytics_service import save_search
from app.services.memory_service import (
    memory_to_text,
    get_recent_memory
)
from app.models.chat_model import ChatHistory
from app.services.mongo_service import (
    get_chat_memory,
    save_chat_memory,
    build_memory_context
)

llm = OllamaLLM(
    model="tinyllama",
    base_url=OLLAMA_URL
)

def rag_chat(
    question,
    db,
    user_id,
    top_k=3
):
    print("start")

    results = hybrid_search(question)

    context = ""

    for item in results["elastic_results"]:
        context += (
            item["_source"]["content"]
            + "\n"
        )

    for doc in results["vector_results"]:
        context += (
            doc.page_content
            + "\n"
        )

    previous_chats = get_recent_memory(
        db,
        user_id,
        limit=5
    )

    memory_text = memory_to_text(
        previous_chats
    )

    memory = get_chat_memory(
        user_id
    )

    memory_context = build_memory_context(
        memory
    )

    prompt = f"""
Previous Conversation:

{memory_context}

Context:

{context}

Question:

{question}

Answer clearly.
"""

    answer = llm.invoke(prompt)

    save_chat_memory(
        user_id,
        question,
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
        user_id=user_id
    )

    print("reached")

    db.add(chat)
    db.commit()

    print("store")

    return {
        "answer": answer,
        "context": context
    }