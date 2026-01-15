from sqlmodel import Session
from ..models import Commune
from ..repositories import CommuneRepository

class CommuneService:
    def __init__(self):
        self.repo = CommuneRepository()

    def get_all(self, db: Session):
        return self.repo.get_all(db)

    def get_by_id(self, db: Session, id: int):
        return self.repo.get_by_id(db, id)

    def create(self, db: Session, commune: Commune):
        return self.repo.create(db, commune)

    def patch(self, db: Session, id: int, updates: dict):
        return self.repo.patch(db, id, updates)

    def delete(self, db: Session, id: int):
        return self.repo.delete(db, id)
