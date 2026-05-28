def supervisor_agent(query):
        query = query.lower()

        if "summary" in query:
                return "summary"
        
        return "search"
#supervisor agent will decide which agent should run