
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
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
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # facultatif

    # --------------------------
    # Configuration Pydantic v2
    # --------------------------
    model_config = {
        "env_file": ".env",
        "extra": "allow",  # permet d'avoir d'autres variables dans le .env
        "case_sensitive": True,  # sensible à la casse
    }


# Instance globale à utiliser partout
settings = Settings()
