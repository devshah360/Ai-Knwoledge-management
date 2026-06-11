from fastapi import APIRouter
from app.database import Session_local
from redis import Redis
from elasticsearch import Elasticsearch

from app.models.user_model import User
from app.models.document_model import Document
from app.models.chat_model import ChatHistory
from app.models.search_model import SearchHistory
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db

import psutil








router = APIRouter(
    prefix="/monitoring",
    tags=["Monitoring"]
)
@router.get("/status")
def status():

    return {
        "api":"running",
        "elastic":"running",
        "mongo":"running",
        "redis":"running"
    }

@router.get("/health")
def health():

    status = {}

    status["api"] = "running"

    try:
        db = Session_local()
        db.execute("SELECT 1")
        status["database"] = "running"
    except:
        status["database"] = "down"
    finally:
        db.close()

    try:
        redis_client = Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )
        redis_client.ping()
        status["redis"] = "running"
    except:
        status["redis"] = "down"

    
    try:
        es = Elasticsearch("https://localhost:9200")
        status["elasticsearch"] = ("running"
        if  es.ping()
        else "down"
        )
    except:
        status["elasticsearch"] = "down"

    return status

@router.get("/metrics")
def metrics(db:Session=Depends(get_db)):
    return {
        "users": db.query(User).count(),
        "documents": db.query(Document).count(),
        "chats": db.query(ChatHistory).count(),
        "searches": db.query(SearchHistory).count()
    }

@router.get("/resources")
def resources():

    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": memory.percent,
        "memory_used_db": round(memory.used / (1024**3) ,2),
        "memory_total_db": round(memory.total / (1024**3) ,2),
        "disk_percent": disk.percent,
        "disk_used_db": round(disk.used / (1024**3) ,2),
        "disk_total_db": round(disk.total / (1024**3) ,2),
    }
