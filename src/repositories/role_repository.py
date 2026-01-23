from typing import List, Optional
from sqlmodel import Session, select
from src.models import Role, RoleRead, RoleName
from src.core.exceptions import NotFoundException


class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_list_role(self) -> List[RoleRead]:
        """Récupère la liste de toutes les roles."""
        return self.db.query(Role).all()

    def get_by_id(self, idrole: int) -> Optional[Role]:
        #return self.db.get(Role, idrole)
        statement = select(Role).where(Role.id == idrole)
        role = self.db.exec(statement).first()
        if not role:
            # On gère l'erreur d'existence directement ici ou dans le service
            raise NotFoundException(f"Le rôle avec l'ID {idrole} n'existe pas.")
        return role
    
    def get_by_name(self, name: RoleName) -> Optional[Role]:
        """Recherche un rôle par son libellé (librole)."""
        statement = select(Role).where(Role.librole == name)
        return self.db.exec(statement).first()

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

    def delete(self, idrole: int) -> bool:
        role = self.get_by_id(idrole) 
        self.db.delete(role)
        self.db.commit()
        return True


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
