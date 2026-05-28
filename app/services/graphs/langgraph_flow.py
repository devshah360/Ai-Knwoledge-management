from typing import TypedDict
from langgraph.graph import StateGraph,END
from app.services.agents.responses_agent import response_agent
from app.services.agents.search_agent import search_agent
from app.services.agents.summary_agent import summary_agent
from app.services.agents.supervisor_agent import supervisor_agent

class AgentState(TypedDict):
        question : str
        context : str
        answer : str

def search_node(state):
        result = search_agent(state["question"])
        return {"context": result["context"]}

def response_node(state):
        answer = response_agent(state["question"],state["context"])
        return{"answer": answer}

graph = StateGraph(AgentState)

graph.add_node("search",search_node)
graph.add_node("response",response_node)

graph.set_entry_point("search")

graph.add_edge("search","response")
graph.add_edge("response",END)

workflow = graph.compile()
