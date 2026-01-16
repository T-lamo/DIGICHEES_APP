from fastapi import APIRouter, Depends, Path, status, Query
from sqlmodel import Session

from src.conf.db.database import Database
from src.models import Vignette, VignetteBase, VignetteRead, VignettePatch
from src.services.vignette_service import VignetteService

router = APIRouter(prefix="/vignettes", tags=["vignettes"])

# ---------------------------
# Dépendance pour le service
# ---------------------------
def get_vignette_service(
    db: Session = Depends(Database.get_session)
) -> VignetteService:
    return VignetteService(db)


# ---------------------------
# ROUTES
# ---------------------------

# LISTE PAGINÉE
@router.get("/", response_model=dict)
def list_vignettes(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: VignetteService = Depends(get_vignette_service)
):
    """
    Liste paginée de toutes les vignettes.
    Gestion des erreurs centralisée via le handler global.
    """
    return service.list_vignettes(limit, offset)


# GET BY ID
@router.get("/{idvignette}", response_model=VignetteRead)
def get_vignette(
    idvignette: int = Path(..., title="ID de la vignette"),
    service: VignetteService = Depends(get_vignette_service)
):
    """
    Récupère une vignette par son ID.
    Si non trouvée, NotFoundException levée et gérée globalement.
    """
    return service.get_vignette(idvignette)


# CREATE
@router.post(
    "/",
    response_model=VignetteRead,
    status_code=status.HTTP_201_CREATED
)
def create_vignette(
    data: VignetteBase,
    service: VignetteService = Depends(get_vignette_service)
):
    """
    Création d'une nouvelle vignette.
    Les violations de contraintes sont transformées en exceptions centralisées.
    """
    return service.create_vignette(data)


# UPDATE / PATCH
@router.patch("/{idvignette}", response_model=VignettePatch)
def update_vignette(
    idvignette: int,
    data: VignettePatch,
    service: VignetteService = Depends(get_vignette_service)
):
    """
    Mise à jour d'une vignette existante.
    Si ID non trouvé → NotFoundException
    Si violation DB → ConflictException / BadRequestException
    """
    return service.update_vignette(idvignette, data)


# DELETE
@router.delete(
    "/{idvignette}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_vignette(
    idvignette: int,
    service: VignetteService = Depends(get_vignette_service)
):
    """
    Suppression d'une vignette.
    Les erreurs sont automatiquement gérées par le handler global.
    """
    service.delete_vignette(idvignette)
