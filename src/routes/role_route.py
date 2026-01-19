from fastapi import APIRouter, Depends, Path, status, Query
from sqlmodel import Session
from src.conf.db.database import Database
from src.models import Role, RoleBase, RoleRead, RolePatch
from src.services.role_service import RoleService

router = APIRouter(prefix="/roles", tags=["roles"])

# ---------------------------
# Dépendance pour le service
# ---------------------------
def get_role_service(
    db: Session = Depends(Database.get_session)
) -> RoleService:
    return RoleService(db)


# ---------------------------
# ROUTES
# ---------------------------

# LISTE PAGINÉE
@router.get("/", response_model=dict)
def list_roles(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: RoleService = Depends(get_role_service)
):
    """
    Liste paginée de toutes les roles.
    Gestion des erreurs centralisée via le handler global.
    """
    return service.list_roles(limit, offset)


# GET BY ID
@router.get("/{idrole}", response_model=RoleRead)
def get_role(
    idrole: int = Path(..., title="ID de la role"),
    service: RoleService = Depends(get_role_service)
):
    """
    Récupère une role par son ID.
    Si non trouvée, NotFoundException levée et gérée globalement.
    """
    return service.get_role(idrole)


# CREATE
@router.post(
    "/",
    response_model=RoleRead,
    status_code=status.HTTP_201_CREATED
)
def create_role(
    data: RoleBase,
    service: RoleService = Depends(get_role_service)
):
    """
    Création d'une nouvelle role.
    Les violations de contraintes sont transformées en exceptions centralisées.
    """
    return service.create_role(data)


# UPDATE / PATCH
@router.patch("/{idrole}", response_model=RolePatch)
def update_role(
    idrole: int,
    data: RolePatch,
    service: RoleService = Depends(get_role_service)
):
    """
    Mise à jour d'une role existante.
    Si ID non trouvé → NotFoundException
    Si violation DB → ConflictException / BadRequestException
    """
    return service.update_role(idrole, data)


# DELETE
@router.delete(
    "/{idrole}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_role(
    idrole: int,
    service: RoleService = Depends(get_role_service)
):
    """
    Suppression d'une role.
    Les erreurs sont automatiquement gérées par le handler global.
    """
    service.delete_role(idrole)
