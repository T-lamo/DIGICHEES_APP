import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # --------------------------
    # Environment
    # --------------------------
    ENV: str = "dev"

    # --------------------------
    # Database
    # --------------------------
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "digichees_db"

    # --------------------------
    # JWT
    # --------------------------
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --------------------------
    # Pydantic v2 config
    # --------------------------
    model_config = {
        "env_file": f".env.{os.getenv('ENV', 'dev')}",
        "extra": "allow",
        "case_sensitive": True,
    }


settings = Settings()
