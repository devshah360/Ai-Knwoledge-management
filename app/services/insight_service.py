from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="tinyllama")

def generate_dashboard_insight(stats):
        prompt = f"""

        Analyze these business metrics:

        {stats}

        Generate short AI insights about platform usage."""

        insight = llm.invoke(prompt)

        return insight

from app.services.insight_service import (
    generate_dashboard_insight
)

def generate_insights(db):

    return {
        "most_used_feature": "chat",
        "most_active_agent": "search_agent",
        "top_search": "FastAPI"
    }