from sqlalchemy import Column,Integer,String
from app.database import Base

class ProcessingTask(Base):
        __tablename__ = "processing_tasks"

        id = Column(Integer,primary_key=True,index=True)

        task_id = Column(String)

        status = Column(String)