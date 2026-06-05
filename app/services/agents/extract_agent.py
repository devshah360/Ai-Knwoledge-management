from langchain_ollama import OllamaLLM

llm = OllamaLLM(
        model = "qwen2.5:3b",
)

def extract_key_points(text):
        prompt = f"""
        Extract :

        -important concepts
        -technologies
        -skils

        Content:

        {text}
        """

        return llm.invoke(prompt)