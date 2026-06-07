from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy.sql import func
from app.database import Base

class SearchHistory(Base):
        __tablename__ = "search_history"

        id = Column(Integer,primary_key=True)

        query = Column(String)

        created_at = Column(DateTime,server_default=func.now())