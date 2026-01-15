from typing import List
from fastapi import APIRouter, Depends, Path, status
from sqlmodel import Session

from src.conf.db.database import Database
from src.models.exemple_model import Exemple
from src.services.exemple_service import ExempleService

router = APIRouter(prefix="/exemples", tags=["exemples"])


# ---------------------------
# Dépendance pour le service
# ---------------------------
def getExempleService() -> ExempleService:
    session = Session(Database.get_engine())
    return ExempleService(session)


@router.get("/", response_model=list[Exemple])
def list_exemples(service: ExempleService = Depends(getExempleService)):
    return service.list_users()
