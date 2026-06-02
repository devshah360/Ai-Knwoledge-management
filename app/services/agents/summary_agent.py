from langchain_ollama import OllamaLLM

llm = OllamaLLM(
        model="tinyllama"
)

def summary_agent(text):
        prompt = f"""
        Summarize this content clearly:

        {text}
        """

        return llm.invoke(prompt) 