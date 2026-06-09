from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models.user_model import User
from app.routes.user_routes import router as user_router
from app.routes.auth_routes import router as auth_router
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.middlewave.auth_middleware import get_current_user,admin_required,manager_required
from app.models.document_model import Document
from app.routes.document_routes import router as document_router
from app.routes.serach_routes import router as serach_router
from app.routes.semantic_routes import router as semantic_router
from app.routes.chat_routes import router as chat_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.serach_routes import router as search_router
from app.routes.history_routes import router as history_router
from app.routes.knowledge_routes import router as knowledge_router
from app.routes.activity_routes import router as activity_router
from app.routes.admin_routes import router as admin_router
from app.routes.user_dashboard import router as current_user_router
from app.utils.exception_handler import global_exception_handler
from app.middlewave.logging_middleware import LoggingMiddleware
from app.core.rate_limit import limiter
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.migration_routes import router as migration_router
from app.routes.monitoring_routes import router as monitoring_router
from app.middlewave.metrics_middleware import MetricsMiddleware
from app.routes.system_routes import router as system_router
from app.routes.sync_dashboard_routes import router as sync_dashboard_router
from app.routes.graph_routes import router as graph_router
from fastapi import UploadFile,File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
import asyncio



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging Middleware
app.add_middleware(LoggingMiddleware)

# API Versioning
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(document_router)
app.include_router(serach_router)
app.include_router(semantic_router)
app.include_router(chat_router)
app.include_router(dashboard_router)
app.include_router(search_router)
app.include_router(history_router)
app.include_router(knowledge_router)
app.include_router(activity_router)
app.include_router(admin_router)
app.include_router(current_user_router)
app.include_router(dashboard_router)
app.include_router(monitoring_router)
app.include_router(migration_router)
app.include_router(system_router)
app.include_router(sync_dashboard_router)
app.include_router(graph_router)

app.add_middleware(
    MetricsMiddleware
)
# Global Exception Handler
app.add_exception_handler(
    Exception,
    global_exception_handler
)

# Rate Limiter
app.state.limiter = limiter

app.mount(
    "/files",
    StaticFiles(directory="app/uploads"),
    name="files"
)

@app.get("/")
def home():
    return {
        "message": "AI Knowledge Management API"
    }


@app.get("/protected")
def protected_route(
    token: str = Depends(oauth2_scheme)
):
    return {
        "message": "protected route",
        "token": token
    }


@app.get("/me")
def get_me(
    current_user=Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role
    }


@app.get("/admin")
def admin_dashboard(
    current_user=Depends(admin_required)
):
    return {
        "messsage": f"Welcome Admin {current_user.username}"

    }


@app.get("/manager")
def manager_dashboard(
    current_user=Depends(manager_required)
):
    return {
        "message": "Manager Dashboard"
    }
@app.post("/documents/upload")
async def upload_document(file: UploadFile = File (...)):
    return {
        "filename": file.filename,
        "status": "uploaded"
    }

@app.get("/dashboard/stats")
def dashboard_stats():

    return {
        "documents": 250,
        "users": 35,
        "queries": 8200,
        "tasks": 15
    }

@app.get("/dashboard/search-analytics")
def search_analytics():

    return [
        {"day":"Mon","count":120},
        {"day":"Tue","count":160},
        {"day":"Wed","count":180},
        {"day":"Thu","count":220},
        {"day":"Fri","count":200}
    ]

@app.get("/dashboard/upload-analytics")
def upload_analytics():

    return [
        {"month":"Jan","count":50},
        {"month":"Feb","count":75},
        {"month":"Mar","count":120},
        {"month":"Apr","count":180},
        {"month":"May","count":250}
    ]
@app.get("/chat/history")
def get_chat_history():

    return [
        {
            "id": 1,
            "title":
                "Leave Policy",
            "created_at":
                "2025-06-01"
        },
        {
            "id": 2,
            "title":
                "Travel Policy",
            "created_at":
                "2025-06-02"
        }
    ]

@app.get("/chat/history/{chat_id}")
def get_chat(chat_id: int):

    return {
        "id": chat_id,

        "messages": [

            {
                "role": "user",
                "content":
                    "Leave Policy?"
            },

            {
                "role": "assistant",
                "content":
                    "12 casual leaves"
            }

        ]
    }

@app.delete("/chat/history/{chat_id}")
def delete_chat(chat_id: int):

    return {
        "message":
            "deleted"
    }

@app.post("/login")
def login():

    return {
        "access_token":
            "jwt_token_here",

        "role":
            "admin"
    }

@app.get("/users/me")
def current_user():

    return {
        "id": 1,

        "name":
            "Admin User",

        "email":
            "admin@test.com",

        "role":
            "admin"
    }

@app.post("/chat/stream")
async def stream_chat():
    async def generate():

        text = """
        Employee receive
        12 casual leaves,
        12 sick leave,
        and 15 annual leaves,
        """

        for word in text.split():

            yield word + " "

            await asyncio.sleep(0.1)

    return StreamingResponse(
        generate(),
        media_type="text/plain"
        )