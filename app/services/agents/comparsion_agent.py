from langchain_ollama import OllamaLLM

llm = OllamaLLM(
        model="tinyllama"
)

def compare_document(doc1,doc2):
        prompt=f"""

        Compare:

        Document 1:
        {doc1}

        Document 2:
        {doc2}

        Show similarites and differences."""

        return llm.invoke(prompt)
