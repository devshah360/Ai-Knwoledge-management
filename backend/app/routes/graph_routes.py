from fastapi import APIRouter
from app.services.agents.workflow_agent import workflow
from fastapi.responses import FileResponse

router = APIRouter(
    prefix="/graph",
    tags=["Graph"]
)

@router.get("/graph")
def graph_image():
        graph = workflow.get_graph()

        png_bytes = graph.draw_mermaid_png()

        with open("graph.png","wb") as f:
                f.write(png_bytes)

        return {"message": "graph generated"}

@router.get("/graph-view")
def graph_view():
        return FileResponse("graph.png")