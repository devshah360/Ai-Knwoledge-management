from app.services.graphs.langgraph_flow import workflow

def run_workflow(question):
    route = route_query(question)

    result = workflow.invoke({
        "question": question
    })

    return {
        "route": route,
        "result": result
    }