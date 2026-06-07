import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

SECRET_KEY = os.getenv("SECRET_KEY")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

ELASTIC_URL = os.getenv("ELASTIC_URL")

MONGO_URL = os.getenv("MONGO_URL")

REDIS_URL = os.getenv("REDIS_URL")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

