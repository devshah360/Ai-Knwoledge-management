from passlib.context import CryptContext
from jose import JWTError,jwt
from datetime import datetime,timedelta
from app.config import(
        SECRET_KEY,
        ALGORITHM,
        ACCESS_TOKEN_EXPIRE_MINUTES
)

pwd_context = CryptContext(
        schemes=["bcrypt"],
        deprecated = "auto"
)

def hash_password(password:str):
        return pwd_context.hash(password)

def verify_password(
        plain_password,
        hashed_password
):
        return pwd_context.verify(
                plain_password,
                hashed_password
        )



def create_access_token(data:dict): #whole code is for user authentication

        to_encode = data.copy()

        expire = datetime.utcnow() + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode.update({"exp":expire})

        encode_jwt = jwt.encode(
                to_encode,
                SECRET_KEY,
                algorithm=ALGORITHM
        )
        return encode_jwt