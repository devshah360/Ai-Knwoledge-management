from langchain_ollama import OllamaLLM

llm = OllamaLLM(
        model="tinyllama"
)

def compare_document(doc1, doc2):
    print("DOC1:", doc1[:500])
    print("DOC2:", doc2[:500])

        Compare:

Document 1:
{doc1}

Document 2:
{doc2}

Only use information from these documents.
Show:
1. Similarities
2. Differences
"""

    print(prompt[:2000])

    return llm.invoke(prompt)

