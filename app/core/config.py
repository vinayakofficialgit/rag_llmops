
import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    DB_HOST=os.getenv("DB_HOST")
    DB_USER=os.getenv("DB_USER")
    DB_PASSWORD=os.getenv("DB_PASSWORD")
    DB_NAME=os.getenv("DB_NAME")

    OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL=os.getenv("OPENAI_MODEL")
    

    LANGFUSE_PUBLIC_KEY=os.getenv("LANGFUSE_PUBLIC_KEY")
    LANGFUSE_SECRET_KEY=os.getenv("LANGFUSE_SECRET_KEY")
    LANGFUSE_HOST=os.getenv("LANGFUSE_HOST")

settings = Settings()
