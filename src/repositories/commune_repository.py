from typing import List, Optional
from sqlmodel import Session, select
from src.models import Commune, CommuneRead

class CommuneRepository:
    def __init__(self, db: Session):
        self.db = db

    # Liste de toutes les communes
    def get_list_communes(self) -> List[CommuneRead]:
        return self.db.query(Commune).all()

    # Récupération par ID
    def get_by_id(self, idcommune: int) -> Optional[Commune]:
        return self.db.get(Commune, idcommune)

    # Création
    def create(self, data: Commune) -> Commune:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # Mise à jour
    def update(self, data: Commune) -> Commune:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # Suppression
    def delete(self, data: Commune) -> None:
        self.db.delete(data)
        self.db.commit()

    # Pagination
    def get_paginated(self, limit: int, offset: int) -> List[Commune]:
        statement = select(Commune).limit(limit).offset(offset)
        return self.db.exec(statement).all()

    # Count
    def count(self) -> int:
        statement = select(Commune)
        return len(self.db.exec(statement).all())
