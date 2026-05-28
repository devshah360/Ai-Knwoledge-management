from fastapi import FastAPI
from app.database import engine,Base
from app.models.user_model import User
from app.routes.user_routes import router as user_router
from app.routes.auth_routes import router as auth_router
from fastapi.security import OAuth2PasswordBearer #jwt ke token ko access karta hai (user ko token milne ke baad usko database mai store karne ka kaam karta hai)
from fastapi import Depends
from app.middlewave.auth_middleware import get_current_user
from app.middlewave.auth_middleware import admin_required
from app.middlewave.auth_middleware import manager_required
from app.models.document_model import Document
from app.routes.document_routes import router as document_router
from app.routes.serach_routes import router as serach_router
from app.routes.semantic_routes import router as semantic_router
from app.routes.chat_routes import router as chat_router
from app.routes.dashboard_routes import router as dashboard_router

oauth2_scheme = OAuth2PasswordBearer(
        tokenUrl = "/auth/login"
)

Base.metadata.create_all(bind=engine) #creating database tables

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(document_router)
app.include_router(serach_router)
app.include_router(semantic_router)
app.include_router(chat_router)
app.include_router(dashboard_router)


@app.get("/")
def home():
        return {"message":"AI Knowledge Management API"}

@app.get("/protected")
def protected_route( token: str = Depends(oauth2_scheme)):

        return {
                "message":"protected route",
                "token" : token 
        }

@app.get("/me")
def get_me(current_user = Depends(get_current_user)):
        return{
                "id" : current_user.id,
                "username" : current_user.username,
                "email":current_user.email,
                "role":current_user.role
        }
@app.get("/admin")
def admin_dashboard(current_user = Depends(admin_required)):
        return {
                "messsage" : f" Welcome Admin {current_user.username}"
        }

@app.get("/manager")
def manager_dahboard(
        current_user = Depends(manager_required)
):
        return{
                "message": "Manager Dashboard"
        }
         