from typing import List
from fastapi import APIRouter, Depends, Path, status, Query
from sqlmodel import Session

from src.conf.db.database import Database
from src.models import Conditionnement, ConditionnementBase, ConditionnementRead, ConditionnementPatch
from src.services.conditionnement_service import ConditionnementService

router = APIRouter(prefix="/conditionnements", tags=["conditionnements"])

# ---------------------------
# Dépendance pour le service
# ---------------------------
def get_conditionnement_service(db: Session = Depends(Database.get_session)) -> ConditionnementService:
    return ConditionnementService(db)


# ---------------------------
# ROUTES
# ---------------------------

# LISTE PAGINÉE
@router.get("/", response_model=dict)
def list_conditionnements(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: ConditionnementService = Depends(get_conditionnement_service)
):
    """
    Liste paginée de tous les conditionnements.
    Gestion des erreurs centralisée via le handler global.
    """
    return service.list_conditionnements(limit, offset)


# GET BY ID
@router.get("/{idcondit}", response_model=ConditionnementRead)
def get_conditionnement(
    idcondit: int = Path(..., title="ID du conditionnement"),
    service: ConditionnementService = Depends(get_conditionnement_service)
):
    """
    Récupère un conditionnement par son ID.
    Si non trouvé, NotFoundException levée et gérée globalement.
    """
    return service.get_conditionnement(idcondit)


# CREATE
@router.post(
    "/",
    response_model=ConditionnementRead,
    status_code=status.HTTP_201_CREATED
)
def create_conditionnement(
    data: ConditionnementBase,
    service: ConditionnementService = Depends(get_conditionnement_service)
):
    """
    Création d'un nouveau conditionnement.
    Les violations de contraintes sont transformées en exceptions centralisées.
    """
    return service.create_conditionnement(data)


# UPDATE / PATCH
@router.put("/{idcondit}", response_model=ConditionnementRead)
def update_conditionnement(
    idcondit: int,
    data: ConditionnementPatch,
    service: ConditionnementService = Depends(get_conditionnement_service)
):
    """
    Mise à jour d'un conditionnement existant.
    Si ID non trouvé → NotFoundException
    Si violation DB → ConflictException / BadRequestException
    """
    return service.update_conditionnement(idcondit, data)


# DELETE
@router.delete(
    "/{idcondit}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_conditionnement(
    idcondit: int,
    service: ConditionnementService = Depends(get_conditionnement_service)
):
    """
    Suppression d'un conditionnement.
    Les erreurs sont automatiquement gérées par le handler global.
    """
    service.delete_conditionnement(idcondit)
