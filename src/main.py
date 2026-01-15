from fastapi import FastAPI
from src.conf.db.database import Database
from contextlib import asynccontextmanager
from src.routes import router
from src.conf.db.settings import settings
from src.core import register_exception_handlers
# from src.routes.user_route import router as user_router
# from src.routes.ticket_router import router as ticket_router    
# from src.routes.tag_router import router as tag_router

print(settings.DB_USER)
print(settings.DB_PASSWORD)


# app.include_router(user_router)
# app.include_router(ticket_router)
# app.include_router(tag_router)



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialisation de la base de données au démarrage de l'application
    print("before yield")
    Database.init_db()
    # Recréer la base de données (supprimer et recréer les tables si besoin)
    # Database.recreate_db()
    yield
    print("after yield")

app = FastAPI(lifespan=lifespan)
app.include_router(router)
register_exception_handlers(app)



# @app.on_event("startup")
# def on_startup():
  
#     print("Application has started")




@app.get("/health")
async def health_check():
    """
    Crée un nouvel utilisateur.

    Le corps de la requête (payload) doit contenir :
    - email
    - full_name
    - age
    - is_active (optionnel)
    """
    return {"status": "ok"}