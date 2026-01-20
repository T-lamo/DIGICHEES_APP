from typing import List
from fastapi import APIRouter, Depends, Path, Query, status
from sqlmodel import Session
from src.conf.db.database import Database
from src.models import DepartementBase, DepartementRead, DepartementPatch
from src.services.departement_service import DepartementService

router = APIRouter(prefix="/departements", tags=["departements"])

def get_departement_service(db: Session = Depends(Database.get_session)) -> DepartementService:
    return DepartementService(db)


@router.get("/", response_model=dict)
def list_departements(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: DepartementService = Depends(get_departement_service)
):
    return service.list_departements_paginated(limit, offset)


@router.get("/{iddepart}", response_model=DepartementRead)
def get_departement(
    iddepart: int = Path(..., title="ID du département"),
    service: DepartementService = Depends(get_departement_service)
):
    return service.get_departement(iddepart)


@router.post("/", response_model=DepartementRead, status_code=status.HTTP_201_CREATED)
def create_departement(
    data: DepartementBase,
    service: DepartementService = Depends(get_departement_service)
):
    return service.create_departement(data)


@router.patch("/{iddepart}", response_model=DepartementPatch)
def update_departement(
    iddepart: int,
    data: DepartementPatch,
    service: DepartementService = Depends(get_departement_service)
):
    return service.update_departement(iddepart, data)


@router.delete("/{iddepart}", status_code=status.HTTP_204_NO_CONTENT)
def delete_departement(
    iddepart: int,
    service: DepartementService = Depends(get_departement_service)
):
    service.delete_departement(iddepart)
