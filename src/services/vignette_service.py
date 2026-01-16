from typing import Any, Dict, List
from sqlmodel import Session

from src.repositories.vignette_repository import VignetteRepository
from src.models import VignetteRead, Vignette, VignetteBase, VignettePatch
from src.core import NotFoundException, BadRequestException


class VignetteService:
    def __init__(self, db: Session):
        self.repo = VignetteRepository(db)

    # ------------------------
    # LIST ALL
    # ------------------------
    def list_vignette(self) -> List[VignetteRead]:
        return self.repo.get_list_vignette()

    # ------------------------
    # PAGINATION
    # ------------------------
    def list_vignettes(
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
    def get_vignette(self, idvignette: int) -> Vignette:
        obj = self.repo.get_by_id(idvignette)
        if not obj:
            raise NotFoundException(f"Vignette {idvignette} introuvable")
        return obj

    # ------------------------
    # CREATE
    # ------------------------
    def create_vignette(
        self, data: VignetteBase
    ) -> Vignette:
        try:
            obj = Vignette(**data.model_dump())
            return self.repo.create(obj)
        except Exception as e:
            raise BadRequestException(str(e))

    # ------------------------
    # UPDATE / PATCH
    # ------------------------
    def update_vignette(
        self, idvignette: int, data: VignettePatch
    ) -> Vignette:
        obj = self.get_vignette(idvignette)

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
    def delete_vignette(self, idvignette: int) -> None:
        obj = self.get_vignette(idvignette)
        try:
            self.repo.delete(obj)
        except Exception as e:
            raise BadRequestException(str(e))
