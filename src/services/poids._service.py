from sqlmodel import Session
from ..models import Poids
from ..repositories import PoidsRepository

class PoidsService:
    def __init__(self):
        self.repo = PoidsRepository()

    def get_all(self, db: Session):
        return self.repo.get_all(db)

    def get_by_id(self, db: Session, id: int):
        return self.repo.get_by_id(db, id)

    def create(self, db: Session, poids: Poids):
        return self.repo.create(db, poids)

    def patch(self, db: Session, id: int, updates: dict):
        return self.repo.patch(db, id, updates)

    def delete(self, db: Session, id: int):
        return self.repo.delete(db, id)