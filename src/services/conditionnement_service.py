from typing import Any, Dict, List
from sqlmodel import Session
from src.repositories.conditionnement_repository import ConditionnementRepository
from src.models import ConditionnementRead, Conditionnement, ConditionnementBase, ConditionnementPatch
from src.core import NotFoundException, BadRequestException


class ConditionnementService:
    def __init__(self, db: Session):
        self.repo = ConditionnementRepository(db)

    # ------------------------
    # LIST ALL
    # ------------------------
    def list_conditionnement(self) -> List[ConditionnementRead]:
        return self.repo.get_list_conditionnement()

    # ------------------------
    # PAGINATION
    # ------------------------
    def list_conditionnements(
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
    def get_conditionnement(self, idcondit: int) -> Conditionnement:
        obj = self.repo.get_by_id(idcondit)
        if not obj:
            raise NotFoundException(f"Conditionnement {idcondit} introuvable")
        return obj

    # ------------------------
    # CREATE
    # ------------------------
    def create_conditionnement(
        self, data: ConditionnementBase
    ) -> Conditionnement:
        try:
            obj = Conditionnement(**data.model_dump())
            return self.repo.create(obj)
        except Exception as e:
            # Exemple : violation de contrainte unique ou autre erreur DB
            raise BadRequestException(str(e))

    # ------------------------
    # UPDATE / PATCH
    # ------------------------
    def update_conditionnement(
        self, idcondit: int, data: ConditionnementPatch
    ) -> Conditionnement:
        obj = self.get_conditionnement(idcondit)

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
    def delete_conditionnement(self, idcondit: int) -> None:
        obj = self.get_conditionnement(idcondit)
        try:
            self.repo.delete(obj)
        except Exception as e:
            raise BadRequestException(str(e))
