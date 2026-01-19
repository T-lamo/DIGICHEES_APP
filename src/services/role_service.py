from typing import Any, Dict, List
from sqlmodel import Session

from src.repositories.role_repository import RoleRepository
from src.models import RoleRead, Role, RoleBase, RolePatch, RoleName
from src.core import NotFoundException, BadRequestException


class RoleService:
    def __init__(self, db: Session):
        self.repo = RoleRepository(db)

    # ------------------------
    # LIST ALL
    # ------------------------
    def list_role(self) -> List[RoleRead]:
        return self.repo.get_list_role()

    # ------------------------
    # PAGINATION
    # ------------------------
    def list_roles(
        self, limit: int, offset: int
    ) -> Dict[str, Any]:
        items = self.repo.get_paginated(limit, offset)
        total = self.repo.count()

        return {
            "limit": limit,
            "offset": offset,
            "total": total,
            "data": items
        }

    # ------------------------
    # GET BY ID
    # ------------------------
    def get_role(self, idrole: int) -> Role:
        obj = self.repo.get_by_id(idrole)
        if not obj:
            raise NotFoundException(f"Role {idrole} introuvable")
        return obj

    # ------------------------
    # CREATE
    # ------------------------
    # def create_role(
    #     self, data: RoleBase
    # ) -> Role:
    #     try:
    #         obj = Role(**data.model_dump())
    #         return self.repo.create(obj)
    #     except Exception as e:
    #         raise BadRequestException(str(e))
    def create_role(self, data: RoleBase) -> Role:
            try:
                # La validation se fait déjà via l'Enum dans le modèle RoleBase
                obj = Role(**data.model_dump())
                return self.repo.create(obj)
            except Exception as e:
                # Capture les erreurs si le libellé n'est pas Admin, Operateur colis ou Stock
                raise BadRequestException(f"Impossible de créer le rôle. Détail: {str(e)}")


    # ------------------------
    # UPDATE / PATCH
    # ------------------------
    def update_role(self, idrole: int, data: RolePatch) -> Role:
        # 1. On vérifie d'abord que le rôle existe
        obj = self.get_role(idrole)

        # 2. Mise à jour des champs
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)

        try:
            return self.repo.update(obj)
        except Exception as e:
            raise BadRequestException(f"Erreur lors de la mise à jour du rôle : {str(e)}")
        
    # ------------------------
    # DELETE
    # ------------------------
    def delete_role(self, idrole: int) -> None:
        obj = self.get_role(idrole)
        try:
            self.repo.delete(obj)
        except Exception as e:
            raise BadRequestException(str(e))
