from typing import List, Optional
from sqlmodel import Session, select
from src.models import Role, RoleRead


class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_list_role(self) -> List[RoleRead]:
        """Récupère la liste de toutes les roles."""
        return self.db.query(Role).all()

    def get_by_id(self, idrole: int) -> Optional[Role]:
        return self.db.get(Role, idrole)

    def create(self, data: Role) -> Role:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    def update(self, data: Role) -> Role:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    def delete(self, data: Role) -> None:
        self.db.delete(data)
        self.db.commit()

    def get_paginated(self, limit: int, offset: int) -> List[Role]:
        statement = (
            select(Role)
            .limit(limit)
            .offset(offset)
        )
        return self.db.exec(statement).all()

    def count(self) -> int:
        statement = select(Role)
        return len(self.db.exec(statement).all())
