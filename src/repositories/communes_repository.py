from ..models import Commune
from sqlmodel import Session, select

class CommuneRepository:

    def get_all(self, db: Session):
        return db.exec(select(Commune)).all()

    def get_by_id(self, db: Session, id: int):
        return db.get(Commune, id)

    def create(self, db: Session, commune: Commune):
        db.add(commune)
        db.commit()
        db.refresh(commune)
        return commune

    def patch(self, db: Session, id: int, updates: dict):
        commune = db.get(Commune, id)
        for key, value in updates.items():
            setattr(commune, key, value)
        db.add(commune)
        db.commit()
        db.refresh(commune)
        return commune

    def delete(self, db: Session, id: int):
        commune = db.get(Commune, id)
        db.delete(commune)
        db.commit()
        return commune
