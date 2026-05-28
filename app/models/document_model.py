from sqlalchemy import Column,Integer,String,ForeignKey
from app.database import Base
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy import Text
from sqlalchemy import JSON

class Document(Base):
        __tablename__ = "documents"

        id = Column(Integer,primary_key=True,index=True)

        filename = Column(String)

        filepath = Column(String)

        filetype = Column(String)

        content = Column(Text)

        owner_id = Column(Integer,ForeignKey("users.id"))
        
        created_at = Column(DateTime,default=datetime.utcnow)

        embedding = Column(JSON)

        chunks = Column(JSON)