from typing import Any, Dict, List
from sqlmodel import Session
from src.repositories.departement_repository import DepartementRepository
from src.models import Departement, DepartementBase, DepartementPatch, DepartementRead
from src.core import NotFoundException, BadRequestException

class DepartementService:
    def __init__(self, db: Session):
        self.repo = DepartementRepository(db)

    def list_departements_paginated(self, limit: int, offset: int) -> Dict[str, Any]:
        items = self.repo.get_paginated(limit, offset)
        total = self.repo.count()
        return {"limit": limit, "offset": offset, "total": total, "data": items}

    def get_departement(self, iddepart: int) -> Departement:
        obj = self.repo.get_by_id(iddepart)
        if not obj:
            raise NotFoundException(f"Département {iddepart} introuvable")
        return obj

    def create_departement(self, data: DepartementBase) -> Departement:
        try:
            obj = Departement(**data.model_dump())
            return self.repo.create(obj)
        except Exception as e:
            raise BadRequestException(str(e))

    def update_departement(self, iddepart: int, data: DepartementPatch) -> Departement:
        obj = self.get_departement(iddepart)
        update_data = data.model_dump(exclude_unset=True)
        for k, v in update_data.items():
            setattr(obj, k, v)
        try:
            return self.repo.update(obj)
        except Exception as e:
            raise BadRequestException(str(e))

    def delete_departement(self, iddepart: int) -> None:
        obj = self.get_departement(iddepart)
        try:
            self.repo.delete(obj)
        except Exception as e:
            raise BadRequestException(str(e))
