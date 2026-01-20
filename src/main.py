from fastapi import FastAPI
from src.conf.db.database import Database
from contextlib import asynccontextmanager
from src.routes import router
from src.core import register_exception_handlers
from src.settings import settings
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialisation de la base de données au démarrage de l'application
    Database.init_db()
    # Recréer la base de données (supprimer et recréer les tables si besoin)
    #Database._recreate_db()
    yield
    Database.disconnect()



# Deactivate docs in production
app = FastAPI(
    title="DigiChees API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None if settings.ENV == "prod" else "/docs",
    redoc_url=None if settings.ENV == "prod" else "/redoc",
)

app.include_router(router)
register_exception_handlers(app)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",   # si ton fichier s'appelle main.py
        host="0.0.0.0",
        port=8000,
        reload=True
    )
