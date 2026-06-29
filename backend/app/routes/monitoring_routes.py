from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from redis import Redis
import psutil

from app.database import Session_local, get_db
from app.services.elastic_service import es
from app.services.mongo_service import client as mongo_client
from app.celery_worker import celery

from app.models.user_model import User
from app.models.document_model import Document
from app.models.chat_model import ChatHistory
from app.models.search_model import SearchHistory


router = APIRouter(
    prefix="/monitoring",
    tags=["Monitoring"]
)


@router.get("/health")
def health():

    status = {
        "api": "running"
    }

    # SQL Database
    try:
        db = Session_local()
        db.execute(text("SELECT 1"))
        status["database"] = "running"
    except Exception as e:
        print("Database Error:", e)
        status["database"] = "down"
    finally:
        db.close()

    # Redis
    try:
        redis_client = Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )
        redis_client.ping()
        status["redis"] = "running"
    except Exception as e:
        print("Redis Error:", e)
        status["redis"] = "down"

    # Elasticsearch
    try:
        status["elasticsearch"] = (
            "running"
            if es.ping()
            else "down"
        )
    except Exception as e:
        print("Elasticsearch Error:", e)
        status["elasticsearch"] = "down"

    # MongoDB
    try:
        mongo_client.admin.command("ping")
        status["mongodb"] = "running"
    except Exception as e:
        print("Mongo Error:", e)
        status["mongodb"] = "down"

    # Celery Worker
    try:
        redis_client = Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )

        redis_client.ping()

        status["celery"] = "running"

    except Exception as e:
        print("Celery Error:", e)
        status["celery"] = "down"

    return status


@router.get("/metrics")
def metrics(db: Session = Depends(get_db)):
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
        "memory_used_gb": round(memory.used / (1024 ** 3), 2),
        "memory_total_gb": round(memory.total / (1024 ** 3), 2),
        "disk_percent": disk.percent,
        "disk_used_gb": round(disk.used / (1024 ** 3), 2),
        "disk_total_gb": round(disk.total / (1024 ** 3), 2),
    }