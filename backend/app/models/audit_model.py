from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy.sql import func
from app.database import Base

class AuditLog(Base):
        __tablename__ = "audit_log"

        id = Column(Integer,primary_key=True)

        user_id = Column(Integer)

        action = Column(String)

        created_at = Column(DateTime,server_default=func.now())