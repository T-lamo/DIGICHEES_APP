from typing import Any, Dict, List
from sqlmodel import Session
from src.repositories import ObjetRepository
from src.models import ObjetRead, Objet, ObjetBase, ObjetPatch
from src.core import NotFoundException, BadRequestException


class ObjetService:
    def __init__(self, db: Session):
        self.repo = ObjetRepository(db)

    # ------------------------
    # LIST ALL
    # ------------------------
    def list_objet(self) -> List[ObjetRead]:
        return self.repo.get_list_objet()

    # ------------------------
    # PAGINATION
    # ------------------------
    def list_objets(
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
    def get_objet(self, idcondit: int) -> Objet:
        obj = self.repo.get_by_id(idcondit)
        if not obj:
            raise NotFoundException(f"Objet {idcondit} introuvable")
        return obj

    # ------------------------
    # CREATE
    # ------------------------
    def create_objet(
        self, data: ObjetBase
    ) -> Objet:
        try:
            obj = Objet(**data.model_dump())
            return self.repo.create(obj)
        except Exception as e:
            # Exemple : violation de contrainte unique ou autre erreur DB
            raise BadRequestException(str(e))

    # ------------------------
    # UPDATE / PATCH
    # ------------------------
    def update_objet(
        self, idcondit: int, data: ObjetPatch
    ) -> Objet:
        obj = self.get_objet(idcondit)

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)

        try:
            return self.repo.update(obj)
        except Exception as e:
            raise BadRequestException(str(e))

    # ------------------------
    # DELETE
    # ------------------------
    def delete_objet(self, idcondit: int) -> None:
        obj = self.get_objet(idcondit)
        try:
            self.repo.delete(obj)
        except Exception as e:
            raise BadRequestException(str(e))
