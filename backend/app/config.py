from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    SECRET_KEY: str = "change-this-secret-key"
    BACKEND_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:5173"
    DEMO_MODE: bool = True
    GMAIL_MAX_RESULTS: int = 100

    class Config:
        env_file = ".env"


settings = Settings()
