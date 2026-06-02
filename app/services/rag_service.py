from langchain_ollama import OllamaLLM
from app.services.search_service import hybrid_search
from app.services.search_analytics_service import save_search
from app.services.memory_service import memory_to_text,get_recent_memory
from app.models.chat_model import ChatHistory

llm = OllamaLLM(model="tinyllama")

def rag_chat(question,db,user_id,top_k=3):
    print("start")
    results = hybrid_search(question)

    context = ""
    for item in results["elastic_results"]:
        context += (
            item["_source"]
            ["content"]
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

    memory_text = memory_to_text(previous_chats)

    prompt = f"""
    Conversation History:

    {memory_text}

    Context:

    {context}

    Question:

    {question}

    Answer based on conversational history and provided context."""

    answer = llm.invoke(prompt)
    
    save_search(db,question)

    chat = ChatHistory(question=question,answer=answer,sources="RAG",user_id = user_id)

    print("reached")
    db.add(chat)
    db.commit()
    print("store")
   
    return {
        "answer":answer,
        "context":context
    }

