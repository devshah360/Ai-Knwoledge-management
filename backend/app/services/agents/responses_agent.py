from langchain_ollama import OllamaLLM

llm = OllamaLLM(model = "qwen2.5:3b",)

def response_agent(question,context,memory_text=""):

        prompt = f"""
        Conversation History:
        {memory_text}

        Context:
        {context}

        Question:
        {question}

        Answer clearly using the provided context.
        """
        response = llm.invoke(prompt)

        return response