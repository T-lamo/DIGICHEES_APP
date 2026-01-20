from typing import List
from src.core.logging import log_action
from fastapi import APIRouter, Depends, Path, status, Query, Request
from sqlmodel import Session

from src.conf.db.database import Database
from src.models import Utilisateur, UtilisateurRead, UtilisateurBase, UtilisateurPatch, UtilisateurCreate
from src.services.utilisateur_service import UtilisateurService
from typing_extensions import Annotated
from src.core.auth.auth_dependencies import oauth2_scheme, get_user_sub_from_token


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
    service: UtilisateurService = Depends(get_utilisateur_service),
    request: Request = None
):
    """
    Création d'un utilisateur (PUBLIC)
    """
    # Create user
    new_user = service.create_utilisateur(data)

    # Log the action
    log_action(
        action="create",
        user_id=None,  # no logged-in user for public signup
        resource="utilisateur",
        resource_id=new_user.id,  # ID of the newly created user
        status="success",
        ip=request.client.host if request else None
    )

    return new_user

# ---------------------------
# ROUTES PROTÉGÉES
# ---------------------------

@private_router.get("/", response_model=dict)
def list_utilisateurs(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: UtilisateurService = Depends(get_utilisateur_service),
    token: str = Depends(oauth2_scheme),
    request: Request = None
):
    user_sub = get_user_sub_from_token(token)

    result =  service.list_utilisateurs(limit, offset)
    log_action(
        action="list",
        user_id=user_sub,
        resource="utilisateurs",
        resource_id=None,
        status="success",
        ip=request.client.host if request else None
    )
    return result


@private_router.get("/{idutilisateur}", response_model=UtilisateurRead)
def get_utilisateur(
    idutilisateur: int = Path(..., title="ID du utilisateur"),
    service: UtilisateurService = Depends(get_utilisateur_service),
    token: str = Depends(oauth2_scheme),
    request: Request = None
):
    user_sub = get_user_sub_from_token(token)
    utilisateur = service.get_utilisateur(idutilisateur)

    log_action(
        action="get",
        user_id=user_sub,
        resource="utilisateur",
        resource_id=idutilisateur,
        status="success",
        ip=request.client.host if request else None
    )
    return utilisateur


@private_router.patch("/{idutilisateur}", response_model=UtilisateurPatch)
def update_utilisateur(
    idutilisateur: int,
    data: UtilisateurPatch,
    service: UtilisateurService = Depends(get_utilisateur_service),
    token: str = Depends(oauth2_scheme),
    request: Request = None
):
    user_sub = get_user_sub_from_token(token)
    updated_user = service.update_utilisateur(idutilisateur, data)

    log_action(
        action="update",
        user_id=user_sub,
        resource="utilisateur",
        resource_id=idutilisateur,
        status="success",
        ip=request.client.host if request else None
    )
    return updated_user


@private_router.delete("/{idutilisateur}", status_code=status.HTTP_204_NO_CONTENT)
def delete_utilisateur(
    idutilisateur: int,
    service: UtilisateurService = Depends(get_utilisateur_service),
    token: str = Depends(oauth2_scheme),
    request: Request = None
):
    user_sub = get_user_sub_from_token(token)
    service.delete_utilisateur(idutilisateur)

    log_action(
        action="delete",
        user_id=user_sub,
        resource="utilisateur",
        resource_id=idutilisateur,
        status="success",
        ip=request.client.host if request else None
    )
