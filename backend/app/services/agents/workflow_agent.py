from app.services.graphs.langgraph_flow import workflow

def run_workflow(question):
        result = workflow.invoke({"question":question})
        return result