from typing import List
from fastapi import APIRouter, Depends, Path, status, Query
from sqlmodel import Session

from src.conf.db.database import Database
from src.models import Utilisateur, UtilisateurRead, UtilisateurBase, UtilisateurPatch, UtilisateurCreate
from src.services.utilisateur_service import UtilisateurService
from typing_extensions import Annotated


# ---------------------------
# Dépendance pour le service
# ---------------------------
def get_utilisateur_service(db: Session = Depends(Database.get_session)) -> UtilisateurService:
    return UtilisateurService(db)


# 🔓 PUBLIC ROUTER
public_router = APIRouter(
    prefix="/utilisateurs",
    tags=["utilisateurs"]
)

# 🔒 PROTECTED ROUTER
private_router = APIRouter(
    prefix="/utilisateurs",
    tags=["utilisateurs"],
)

# ---------------------------
# ROUTES PUBLIQUES
# ---------------------------

@public_router.post(
    "/",
    response_model=UtilisateurRead,
    status_code=status.HTTP_201_CREATED
)
def create_utilisateur(
    data: UtilisateurCreate,
    service: UtilisateurService = Depends(get_utilisateur_service)
):
    """
    Création d'un utilisateur (PUBLIC)
    """
    return service.create_utilisateur(data)

# ---------------------------
# ROUTES PROTÉGÉES
# ---------------------------

@private_router.get("/", response_model=dict)
def list_utilisateurs(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: UtilisateurService = Depends(get_utilisateur_service)
):
    return service.list_utilisateurs(limit, offset)


@private_router.get("/{idutilisateur}", response_model=UtilisateurRead)
def get_utilisateur(
    idutilisateur: int = Path(..., title="ID du utilisateur"),
    service: UtilisateurService = Depends(get_utilisateur_service)
):
    return service.get_utilisateur(idutilisateur)


@private_router.patch("/{idutilisateur}", response_model=UtilisateurPatch)
def update_utilisateur(
    idutilisateur: int,
    data: UtilisateurPatch,
    service: UtilisateurService = Depends(get_utilisateur_service)
):
    return service.update_utilisateur(idutilisateur, data)


@private_router.delete(
    "/{idutilisateur}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_utilisateur(
    idutilisateur: int,
    service: UtilisateurService = Depends(get_utilisateur_service)
):
    service.delete_utilisateur(idutilisateur)
