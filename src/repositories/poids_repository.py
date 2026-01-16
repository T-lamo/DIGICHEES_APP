from typing import List, Optional
from sqlmodel import Session, select
from src.models import Poids, PoidsRead

class PoidsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_list_poids(self) -> List[PoidsRead]:
        """Récupère la liste de tous les Poids."""
        return self.db.query(Poids).all()
    

    def get_by_id(self, idpoids: int) -> Optional[Poids]:
        return self.db.get(Poids, idpoids)

    def create(self, data: Poids) -> Poids:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    def update(self, data: Poids) -> Poids:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    def delete(self, data: Poids) -> None:
        self.db.delete(data)
        self.db.commit()
    
    def get_paginated(self, limit: int, offset: int) -> List[Poids]:
        statement = (
            select(Poids)
            .limit(limit)
            .offset(offset)
        )
        return self.db.exec(statement).all()

    def count(self) -> int:
        statement = select(Poids)
        return len(self.db.exec(statement).all())
      