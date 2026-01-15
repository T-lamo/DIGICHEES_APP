from ..models import Poids
from sqlmodel import Session, select

class PoidsRepository:

    def get_all(self, db: Session):
        return db.exec(select(Poids)).all()

    def get_by_id(self, db: Session, id: int):
        return db.get(Poids, id)

    def create(self, db: Session, poids: Poids):
        db.add(poids)
        db.commit()
        db.refresh(poids)
        return poids

    def patch(self, db: Session, id: int, updates: dict):
        poids = db.get(Poids, id)
        for key, value in updates.items():
            setattr(poids, key, value)
        db.add(poids)
        db.commit()
        db.refresh(poids)
        return poids

    def delete(self, db: Session, id: int):
        poids = db.get(Poids, id)
        db.delete(poids)
        db.commit()
        return poids