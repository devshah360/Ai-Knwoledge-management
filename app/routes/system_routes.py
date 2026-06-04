from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.services.agents.workflow_agent import workflow


router = APIRouter(
        prefix="/system",
        tags=["System"]
)

@router.get("/health")
def health():
        return {
                "status":"healthy"
        }

@router.get("/database")
def database_health():
        return {
                "postgre":"running",
                "mongo":"running",
                "elastic":"running",
                "redis":"running"
        }

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