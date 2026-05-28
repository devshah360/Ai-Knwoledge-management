from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="tinyllama")

def generate_dashboard_insight(stats):
        prompt = f"""

        Analyze these business metrics:

        {stats}

        Generate short AI insights about platform usage."""

        insight = llm.invoke(prompt)

        return insight