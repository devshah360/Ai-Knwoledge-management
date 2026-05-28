from sqlalchemy import Column,String,Integer,ForeignKey,DateTime
from sqlalchemy.sql import func
from app.database import Base

class ChatHistory(Base):
        __tablename__ = "chat_history"

        id =  Column(Integer,primary_key=True,index=True)

        question = Column(String)

        answer = Column(String)

        user_id = Column(Integer,ForeignKey("users.id"))

        created_at = Column(DateTime(timezone=True),server_default=func.now())
