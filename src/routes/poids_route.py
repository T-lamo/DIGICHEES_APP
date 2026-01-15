from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from src.conf.db.database import get_session
from src.models.poids import Poids
from src.services.poids_service import PoidsService

router = APIRouter(prefix="/poidss", tags=["poidss"])
service = PoidsService()

@router.get("/", response_model=list[Poids])
def get_poidss(db: Session = Depends(get_session)):
    return service.get_all(db)

@router.get("/{poids_id}", response_model=Poids)
def get_poids(poids_id: int, db: Session = Depends(get_session)):
    poids = service.get_by_id(db, poids_id)
    if not poids:
        raise HTTPException(status_code=404, detail="Poids non trouvée")
    return poids

@router.post("/", response_model=Poids)
def create_poids(poids: Poids, db: Session = Depends(get_session)):
    return service.create(db, poids)

@router.patch("/{poids_id}", response_model=Poids)
def patch_poids(poids_id: int, updates: dict, db: Session = Depends(get_session)):
    poids = service.get_by_id(db, poids_id)
    if not poids:
        raise HTTPException(status_code=404, detail="Poids non trouvée")
    return service.patch(db, poids_id, updates)

@router.delete("/{poids_id}", response_model=Poids)
def delete_poids(poids_id: int, db: Session = Depends(get_session)):
    poids = service.get_by_id(db, poids_id)
    if not poids:
        raise HTTPException(status_code=404, detail="Poids non trouvée")
    return service.delete(db, poids_id)