from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from src.conf.db.database import get_session
from src.models.commune import Commune
from src.services.commune_service import CommuneService

router = APIRouter(prefix="/communes", tags=["communes"])
service = CommuneService()

@router.get("/", response_model=list[Commune])
def get_communes(db: Session = Depends(get_session)):
    return service.get_all(db)

@router.get("/{commune_id}", response_model=Commune)
def get_commune(commune_id: int, db: Session = Depends(get_session)):
    commune = service.get_by_id(db, commune_id)
    if not commune:
        raise HTTPException(status_code=404, detail="Commune non trouvée")
    return commune

@router.post("/", response_model=Commune)
def create_commune(commune: Commune, db: Session = Depends(get_session)):
    return service.create(db, commune)

@router.patch("/{commune_id}", response_model=Commune)
def patch_commune(commune_id: int, updates: dict, db: Session = Depends(get_session)):
    commune = service.get_by_id(db, commune_id)
    if not commune:
        raise HTTPException(status_code=404, detail="Commune non trouvée")
    return service.patch(db, commune_id, updates)

@router.delete("/{commune_id}", response_model=Commune)
def delete_commune(commune_id: int, db: Session = Depends(get_session)):
    commune = service.get_by_id(db, commune_id)
    if not commune:
        raise HTTPException(status_code=404, detail="Commune non trouvée")
    return service.delete(db, commune_id)
