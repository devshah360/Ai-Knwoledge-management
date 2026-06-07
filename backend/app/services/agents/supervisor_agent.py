def supervisor_agent(query):
        query = query.lower()

        if "summary" in query:
               return "summary"
        
        return "search"
#supervisor agent will decide which agent should run
def route_query(query):
        query = query.lower()

        if "compare" in query:
                return "compare"
        
        if "extract" in query:
                return "extract"
        
        if "summary" in query:
                return "summary"
        
        return "search"