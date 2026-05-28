from sqlalchemy import Column,Integer,String,Boolean
from app.database import Base

class User(Base):  #table ko create kiya hai with fields
        __tablename__ = "users"

        id = Column(Integer,primary_key=True)

        username = Column(String)

        email = Column(String,unique=True) 

        password = Column(String) 
        
        role = Column(String,default="user")

        is_active = Column(Boolean,default= True)