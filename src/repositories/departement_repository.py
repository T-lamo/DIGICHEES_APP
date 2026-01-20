from typing import List, Optional
from sqlmodel import Session, select
from src.models import Departement, DepartementRead

class DepartementRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_list_departements(self) -> List[DepartementRead]:
        return self.db.query(Departement).all()

    def get_by_id(self, iddepart: int) -> Optional[Departement]:
        return self.db.get(Departement, iddepart)

    def create(self, data: Departement) -> Departement:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    def update(self, data: Departement) -> Departement:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    def delete(self, data: Departement) -> None:
        self.db.delete(data)
        self.db.commit()

    def get_paginated(self, limit: int, offset: int) -> List[Departement]:
        statement = select(Departement).limit(limit).offset(offset)
        return self.db.exec(statement).all()

    def count(self) -> int:
        statement = select(Departement)
        return len(self.db.exec(statement).all())
