from typing import List
from src.models import CommuneRead, CommuneBase, CommunePatch
from fastapi import APIRouter, Depends, Path, status, Query
from sqlmodel import Session

from src.conf.db.database import Database
from src.services.commune_service import CommuneService

router = APIRouter(prefix="/communes", tags=["communes"])

# ---------------------------
# Dépendance pour le service
# ---------------------------
def get_commune_service(db: Session = Depends(Database.get_session)) -> CommuneService:
    return CommuneService(db)


# ---------------------------
# ROUTES
# ---------------------------

# LISTE PAGINÉE
@router.get("/", response_model=dict)
def list_communes(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: CommuneService = Depends(get_commune_service)
):
    return service.list_communes_paginated(limit, offset)


# GET BY ID
@router.get("/{idcommune}", response_model=CommuneRead)
def get_commune(
    idcommune: int = Path(..., title="ID de la commune"),
    service: CommuneService = Depends(get_commune_service)
):
    return service.get_commune(idcommune)


# CREATE
@router.post("/", response_model=CommuneRead, status_code=status.HTTP_201_CREATED)
def create_commune(
    data: CommuneBase,
    service: CommuneService = Depends(get_commune_service)
):
    return service.create_commune(data)


# UPDATE / PATCH
@router.patch("/{idcommune}", response_model=CommunePatch)
def update_commune(
    idcommune: int,
    data: CommunePatch,
    service: CommuneService = Depends(get_commune_service)
):
    return service.update_commune(idcommune, data)


# DELETE
@router.delete("/{idcommune}", status_code=status.HTTP_204_NO_CONTENT)
def delete_commune(
    idcommune: int,
    service: CommuneService = Depends(get_commune_service)
):
    service.delete_commune(idcommune)
