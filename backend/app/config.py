from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    SECRET_KEY: str = "change-this-secret-key"
    BACKEND_URL: str = "http://localhost:8000"

    class Config:
        env_file = ".env"


settings = Settings()