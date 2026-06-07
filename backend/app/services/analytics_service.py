from app.models.user_model import User
from app.models.document_model import Document
from app.models.chat_model import ChatHistory

def get_dashboard_state(db):
        total_users = db.query(User).count()
        total_documents = db.query(Document).count()
        total_ai_chat = db.query(ChatHistory).count()

        return {
                "total_user":total_users,
                "total_documents":total_documents,
                "total_queries":total_ai_chat,
                "total_ai_chat":total_ai_chat
        }