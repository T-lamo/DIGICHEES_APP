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
        # 1. Préparation de l'objet (Mapping Schéma -> Modèle Table)
        obj = Role(**data.model_dump())

        # 2. Validation de la règle métier (Les 3 rôles DIGICHEES)
        allowed_roles = [r.value for r in RoleName] 
        if obj.librole not in allowed_roles:
            raise BadRequestException(
                f"Le rôle '{obj.librole}' n'est pas reconnu par DIGICHEES. "
                f"Valeurs autorisées : {', '.join(allowed_roles)}"
            )

        # 3. Tentative de création avec gestion d'erreurs (Doublons et autres)
        try:
            # On vérifie si le rôle existe déjà via le repo avant d'insérer (Optionnel mais recommandé)
            existing = self.repo.get_by_name(obj.librole)
            if existing:
                raise BadRequestException(f"Le rôle '{obj.librole}' existe déjà dans le système.")

            return self.repo.create(obj)

        except BadRequestException as e:
            # On laisse passer notre propre exception métier
            raise e
        except Exception as e:
            # On capture les erreurs SQL (comme le Duplicate Entry 1062 si le check précédent échoue)
            raise BadRequestException(f"Erreur lors de la création du rôle : {str(e)}")
        


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
