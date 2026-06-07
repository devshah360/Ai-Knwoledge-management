from sqlalchemy.orm import sessionmaker # session create karne ke liye (session crud operation perform karta hai)
from sqlalchemy import create_engine # create_engine import karke uska obj bana ke usko database se connect karte hai
from sqlalchemy.orm import declarative_base # declarative_base database bana ne ke liye use hota hai (table aur uski fields)
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

Session_local = sessionmaker(
        autocommit = False,
        autoflush= False,
        bind=engine
        )

Base = declarative_base()

def get_db():

        db = Session_local()

        try :
                yield db
        finally:
                db.close()
                
