from app.services.search_service import hybrid_search

def search_agent(query):
        results = hybrid_search(query)

        return results