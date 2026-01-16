from typing import List
from fastapi import APIRouter, Depends, Path, status, Query
from sqlmodel import Session

from src.conf.db.database import Database
from src.models import Poids, PoidsBase, PoidsRead, PoidsPatch
from src.services.poids_service import PoidsService

router = APIRouter(prefix="/poidss", tags=["poidss"])

# ---------------------------
# Dépendance pour le service
# ---------------------------
def get_poids_service(db: Session = Depends(Database.get_session)) -> PoidsService:
    return PoidsService(db)


# ---------------------------
# ROUTES
# ---------------------------

# LISTE PAGINÉE
@router.get("/", response_model=dict)
def list_poidss(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: PoidsService = Depends(get_poids_service)
):
    """
    Liste paginée de tous les poidss.
    Gestion des erreurs centralisée via le handler global.
    """
    return service.list_poidss(limit, offset)


# GET BY ID
@router.get("/{idpoids}", response_model=PoidsRead)
def get_poids(
    idpoids: int = Path(..., title="ID du poids"),
    service: PoidsService = Depends(get_poids_service)
):
    """
    Récupère un poids par son ID.
    Si non trouvé, NotFoundException levée et gérée globalement.
    """
    return service.get_poids(idpoids)


# CREATE
@router.post(
    "/",
    response_model=PoidsRead,
    status_code=status.HTTP_201_CREATED
)
def create_poids(
    data: PoidsBase,
    service: PoidsService = Depends(get_poids_service)
):
    """
    Création d'un nouveau poids.
    Les violations de contraintes sont transformées en exceptions centralisées.
    """
    return service.create_poids(data)


# UPDATE / PATCH
@router.put("/{idpoids}", response_model=PoidsRead)
def update_poids(
    idpoids: int,
    data: PoidsPatch,
    service: PoidsService = Depends(get_poids_service)
):
    """
    Mise à jour d'un poids existant.
    Si ID non trouvé → NotFoundException
    Si violation DB → ConflictException / BadRequestException
    """
    return service.update_poids(idpoids, data)


# DELETE
@router.delete(
    "/{idpoids}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_poids(
    idpoids: int,
    service: PoidsService = Depends(get_poids_service)
):
    """
    Suppression d'un poids.
    Les erreurs sont automatiquement gérées par le handler global.
    """
    service.delete_poids(idpoids)