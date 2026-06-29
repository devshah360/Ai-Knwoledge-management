import time

from langchain_ollama import OllamaLLM

from app.core.config import OLLAMA_URL

from app.services.search_service import hybrid_search

from app.services.search_analytics_service import save_search

from app.models.chat_model import ChatHistory

from app.services.mongo_service import (
    create_conversation,
    add_message
)


llm = OllamaLLM(
    model="qwen2.5:3b",
    base_url=OLLAMA_URL
)


def rag_chat(
    question,
    db,
    conversation_id=None,
    top_k=8
):

    print("\n========== RAG START ==========")

    results = hybrid_search(
        question,
        top_k=top_k
    )

    elastic_results = results.get(
        "elastic_results",
        []
    )

    vector_results = results.get(
        "vector_results",
        []
    )

    seen = set()

    chunks = []

    for item in elastic_results:

        text = item["_source"].get(
            "content",
            ""
        )

        if text and text not in seen:

            seen.add(text)

            chunks.append(text)

    for doc in vector_results:

        text = doc.page_content

        if text and text not in seen:

            seen.add(text)

            chunks.append(text)

    context = "\n\n".join(chunks)

    MAX_CONTEXT_LENGTH = 6000

    if len(context) > MAX_CONTEXT_LENGTH:

        context = context[:MAX_CONTEXT_LENGTH]

    if not context.strip():

        return {

            "answer": "No relevant information found.",

            "context": ""
        }

    prompt = f"""

You are a professional AI assistant.

Answer ONLY using the provided context.

If answer does not exist say:

"I could not find this information in the provided documents."

Context:

{context}

Question:

{question}

Answer:

"""

    answer = llm.invoke(prompt)

    # IMPORTANT FIX

    if not conversation_id:

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

    print("========== RAG END ==========")

    return {

        "conversation_id": conversation_id,

        "answer": answer,

        "context": context

    }