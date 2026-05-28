from langchain_ollama import OllamaLLM
from app.services.vectorstore_service import retrieve_chunks
from app.services.memory_service import save_message,get_memory

llm = OllamaLLM(model="tinyllama")

def rag_chat(question,top_k=3):
    docs = retrieve_chunks(question,top_k)
    context = "\n\n".join([
        doc.page_content
        for doc in docs
    ])

    #memory = get_memory()

    #memory_text = "\n".join([
       # f"{msg['role']}:{msg['content']}"
      #  for msg in memory
       # ])
    
#    Conversation History:
#    {memory_text}
 
    prompt = f"""


    Context:
    {context}

    Question:
    {question}

    Answer clearly using only the provided context.complex"""

    answer = llm.invoke(prompt)

    save_message("user",question)
    save_message("assistant",answer)

    return {
        "answer":answer,
        "sources":[
            doc.page_content[:200]
            for doc in docs
        ]
    }