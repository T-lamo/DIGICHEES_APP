from typing import Any, Dict, List
from fastapi import HTTPException, status
from sqlmodel import Session
from src.repositories.conditionnement_repository import ConditionnementRepository
from src.models import ConditionnementRead, Conditionnement, ConditionnementBase, ConditionnementPatch


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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conditionnement introuvable"
            )
        return obj

    # ------------------------
    # CREATE (model_dump)
    # ------------------------
    def create_conditionnement(
        self, data: ConditionnementBase
    ) -> Conditionnement:
        obj = Conditionnement(
            **data.model_dump()
        )
        return self.repo.create(obj)

    # ------------------------
    # UPDATE / PATCH (model_dump)
    # ------------------------
    def update_conditionnement(
        self, idcondit: int, data: ConditionnementPatch
    ) -> Conditionnement:
        obj = self.get_conditionnement(idcondit)

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(obj, key, value)

        return self.repo.update(obj)

    # ------------------------
    # DELETE
    # ------------------------
    def delete_conditionnement(self, idcondit: int) -> None:
        obj = self.get_conditionnement(idcondit)
        self.repo.delete(obj)
