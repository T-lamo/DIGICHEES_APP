from typing import List, Optional

from sqlmodel import Session, select
from src.models import Conditionnement, ConditionnementRead

class ConditionnementRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_list_conditionnement(self) -> List[ConditionnementRead]:
        """Récupère la liste de tous les Conditionnements."""
        return self.db.query(Conditionnement).all()
    

    def get_by_id(self, idcondit: int) -> Optional[Conditionnement]:
        return self.db.get(Conditionnement, idcondit)

    def create(self, data: Conditionnement) -> Conditionnement:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    def update(self, data: Conditionnement) -> Conditionnement:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    def delete(self, data: Conditionnement) -> None:
        self.db.delete(data)
        self.db.commit()
    
    def get_paginated(self, limit: int, offset: int) -> List[Conditionnement]:
        statement = (
            select(Conditionnement)
            .limit(limit)
            .offset(offset)
        )
        return self.db.exec(statement).all()

    def count(self) -> int:
        statement = select(Conditionnement)
        return len(self.db.exec(statement).all())
      