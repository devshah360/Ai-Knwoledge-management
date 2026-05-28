from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="tinyllama")

def response_agent(question,context):

        prompt = f"""
        Context:
        {context}

        Question:
        {question}

        Answer clearly using the provided context.
        """
        response = llm.invoke(prompt)

        return response