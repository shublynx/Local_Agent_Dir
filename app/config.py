from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    UPLOAD_BASE_DIR: str = "data/uploads"
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
