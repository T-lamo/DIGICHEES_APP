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


# @router.get("/", response_model=List[Conditionnement])
# def list_Conditionnements(service: ConditionnementService = Depends(get_conditionnement_service)):
#     return service.list_conditionnement()


# src/routes/conditionnement_route.py
@router.get("/", response_model=dict)
def list_conditionnements(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: ConditionnementService = Depends(get_conditionnement_service)
):
    return service.list_conditionnements(limit, offset)


@router.get("/{idcondit}", response_model=ConditionnementRead)
def get_conditionnement(
    idcondit: int,
    service: ConditionnementService = Depends(get_conditionnement_service)
):
    return service.get_conditionnement(idcondit)



@router.post(
    "/",
    response_model=ConditionnementRead,
    status_code=status.HTTP_201_CREATED
)
def create_conditionnement(
    data: ConditionnementBase,
    service: ConditionnementService = Depends(get_conditionnement_service)
):
    return service.create_conditionnement(data)

@router.put("/{idcondit}", response_model=ConditionnementRead)
def update_conditionnement(
    idcondit: int,
    data: ConditionnementPatch,
    service: ConditionnementService = Depends(get_conditionnement_service)
):
    return service.update_conditionnement(idcondit, data)

@router.delete(
    "/{idcondit}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_conditionnement(
    idcondit: int,
    service: ConditionnementService = Depends(get_conditionnement_service)
):
    service.delete_conditionnement(idcondit)
