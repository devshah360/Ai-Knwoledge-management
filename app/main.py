from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models.user_model import User
from app.routes.user_routes import router as user_router
from app.routes.auth_routes import router as auth_router
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.middlewave.auth_middleware import (
    get_current_user,
    admin_required,
    manager_required
)
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
from app.routes.dashboard_routes import (
    router as dashboard_router
)
from app.middlewave.metrics_middleware import MetricsMiddleware

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging Middleware
app.add_middleware(LoggingMiddleware)

# API Versioning
app.include_router(user_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(document_router, prefix="/api/v1")
app.include_router(serach_router, prefix="/api/v1")
app.include_router(semantic_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")
app.include_router(search_router, prefix="/api/v1")
app.include_router(history_router, prefix="/api/v1")
app.include_router(knowledge_router, prefix="/api/v1")
app.include_router(activity_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")
app.include_router(current_user_router, prefix="/api/v1")
app.include_router(dashboard_router)
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
def manager_dahboard(
    current_user=Depends(manager_required)
):
    return {
        "message": "Manager Dashboard"
    }