#from typing import TypedDict
#from langgraph.graph import StateGraph,END
#from app.services.agents.responses_agent import response_agent
#from app.services.agents.search_agent import search_agent
#from app.services.agents.summary_agent import summary_agent
#from app.services.agents.supervisor_agent import supervisor_agent

#class AgentState(TypedDict):
 #       question : str
  #      context : str
   #     answer : str

#def search_node(state):
 #       result = search_agent(state["question"])
  #      return {"context": result["context"]}





from typing import TypedDict
from app.services.agents.search_agent import search_agent
from app.services.agents.summary_agent import summary_agent
from app.services.agents.extract_agent import extract_key_points
from langgraph.graph import StateGraph,END
from app.services.agents.responses_agent import response_agent
from app.services.agents.supervisor_agent import route_query
from app.services.agents.supervisor_agent import supervisor_agent

class AgentState(TypedDict):
        question : str
        result : str

def search_node(state):
        result = search_agent(state["question"])
        return {"result": str(result)}

def response_node(state):
        answer = response_agent(state["question"])
        return{"answer": answer}
def summary_node(state):
        result = summary_agent(state["question"])
        return {"result":result}

def extract_node(state):
        result = extract_key_points(state["question"])
        return {"result":result}

def supervisor_node(state):
        return state

def compare_node(state):
        return {"result":"Comparsion logic is here"}

def router(state):
        return route_query(state["question"])

graph = StateGraph(AgentState)

graph.add_node("search",search_node)
graph.add_node("response",response_node)
graph.add_node("summary",summary_node)
graph.add_node("extract",extract_node)
graph.add_node("supervisor", supervisor_node)
graph.add_node("compare",compare_node)

graph.set_entry_point("supervisor")

graph.add_edge("search","response")


graph.add_conditional_edges("supervisor",router,{"search":"search","summary":"summary","extract":"extract","compare":"compare"})
graph.add_edge("search","response")
graph.add_edge("summary",END)
graph.add_edge("extract",END)
graph.add_edge("response",END)

workflow = graph.compile()

