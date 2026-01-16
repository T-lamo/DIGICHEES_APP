from typing import List
from fastapi import APIRouter, Depends, Path, status, Query
from sqlmodel import Session

from src.conf.db.database import Database
from src.models import Objet, ObjetBase, ObjetRead, ObjetPatch
from src.services import ObjetService

router = APIRouter(prefix="/objets", tags=["objets"])

# ---------------------------
# Dépendance pour le service
# ---------------------------
def get_objet_service(db: Session = Depends(Database.get_session)) -> ObjetService:
    return ObjetService(db)


# ---------------------------
# ROUTES
# ---------------------------

# LISTE PAGINÉE
@router.get("/", response_model=dict)
def list_objets(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: ObjetService = Depends(get_objet_service)
):
    """
    Liste paginée de tous les objets.
    Gestion des erreurs centralisée via le handler global.
    """
    return service.list_objets(limit, offset)


# GET BY ID
@router.get("/{idcondit}", response_model=ObjetRead)
def get_objet(
    idcondit: int = Path(..., title="ID du objet"),
    service: ObjetService = Depends(get_objet_service)
):
    """
    Récupère un objet par son ID.
    Si non trouvé, NotFoundException levée et gérée globalement.
    """
    return service.get_objet(idcondit)


# CREATE
@router.post(
    "/",
    response_model=ObjetRead,
    status_code=status.HTTP_201_CREATED
)
def create_objet(
    data: ObjetBase,
    service: ObjetService = Depends(get_objet_service)
):
    """
    Création d'un nouveau objet.
    Les violations de contraintes sont transformées en exceptions centralisées.
    """
    return service.create_objet(data)


# UPDATE / PATCH
@router.put("/{idcondit}", response_model=ObjetRead)
def update_objet(
    idcondit: int,
    data: ObjetPatch,
    service: ObjetService = Depends(get_objet_service)
):
    """
    Mise à jour d'un objet existant.
    Si ID non trouvé → NotFoundException
    Si violation DB → ConflictException / BadRequestException
    """
    return service.update_objet(idcondit, data)


# DELETE
@router.delete(
    "/{idcondit}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_objet(
    idcondit: int,
    service: ObjetService = Depends(get_objet_service)
):
    """
    Suppression d'un objet.
    Les erreurs sont automatiquement gérées par le handler global.
    """
    service.delete_objet(idcondit)
