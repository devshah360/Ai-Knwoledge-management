from pydantic import BaseModel

class Dashboard(BaseModel):
        total_users : int
        total_documents: int
        total_query : int
        total_ai_chats : int
