from typing import List
from fastapi import APIRouter, Depends, Path, status, Query
from sqlmodel import Session

from src.conf.db.database import Database
from src.models import Utilisateur, UtilisateurRead, UtilisateurBase, UtilisateurPatch
from src.services.utilisateur_service import UtilisateurService

router = APIRouter(prefix="/utilisateurs", tags=["utilisateurs"])

# ---------------------------
# Dépendance pour le service
# ---------------------------
def get_utilisateur_service(db: Session = Depends(Database.get_session)) -> UtilisateurService:
    return UtilisateurService(db)


# ---------------------------
# ROUTES
# ---------------------------

# LISTE PAGINÉE
@router.get("/", response_model=dict)
def list_utilisateurs(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: UtilisateurService = Depends(get_utilisateur_service)
):
    """
    Liste paginée de tous les utilisateurs.
    Gestion des erreurs centralisée via le handler global.
    """
    return service.list_utilisateurs(limit, offset)


# GET BY ID
@router.get("/{idutilisateur}", response_model=UtilisateurRead)
def get_utilisateur(
    idutilisateur: int = Path(..., title="ID du utilisateur"),
    service: UtilisateurService = Depends(get_utilisateur_service)
):
    """
    Récupère un utilisateur par son ID.
    Si non trouvé, NotFoundException levée et gérée globalement.
    """
    return service.get_utilisateur(idutilisateur)


# CREATE
@router.post(
    "/",
    response_model=UtilisateurRead,
    status_code=status.HTTP_201_CREATED
)
def create_utilisateur(
    data: UtilisateurBase,
    service: UtilisateurService = Depends(get_utilisateur_service)
):
    """
    Création d'un nouveau utilisateur.
    Les violations de contraintes sont transformées en exceptions centralisées.
    """
    return service.create_utilisateur(data)


# UPDATE / PATCH
@router.patch("/{idutilisateur}", response_model=UtilisateurPatch)
def update_utilisateur(
    idutilisateur: int,
    data: UtilisateurPatch,
    service: UtilisateurService = Depends(get_utilisateur_service)
):
    """
    Mise à jour d'un utilisateur existant.
    Si ID non trouvé → NotFoundException
    Si violation DB → ConflictException / BadRequestException
    """
    return service.update_utilisateur(idutilisateur, data)


# DELETE
@router.delete(
    "/{idutilisateur}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_utilisateur(
    idutilisateur: int,
    service: UtilisateurService = Depends(get_utilisateur_service)
):
    """
    Suppression d'un utilisateur.
    Les erreurs sont automatiquement gérées par le handler global.
    """
    service.delete_utilisateur(idutilisateur)