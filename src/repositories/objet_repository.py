from typing import List, Optional

from sqlmodel import Session, select
from src.models import Objet, ObjetRead

class ObjetRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_list_objet(self) -> List[ObjetRead]:
        """Récupère la liste de tous les Objets."""
        return self.db.query(Objet).all()
    

    def get_by_id(self, codobj: int) -> Optional[Objet]:
        return self.db.get(Objet, codobj)

    def create(self, data: Objet) -> Objet:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    def update(self, data: Objet) -> Objet:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    def delete(self, data: Objet) -> None:
        self.db.delete(data)
        self.db.commit()
    
    def get_paginated(self, limit: int, offset: int) -> List[Objet]:
        statement = (
            select(Objet)
            .limit(limit)
            .offset(offset)
        )
        return self.db.exec(statement).all()

    def count(self) -> int:
        statement = select(Objet)
        return len(self.db.exec(statement).all())
      