from typing import Any, Dict, List
from src.repositories.departement_repository import DepartementRepository
from sqlmodel import Session
from src.repositories.commune_repository import CommuneRepository
from src.models import CommuneRead, Commune, CommuneBase, CommunePatch
from src.core import NotFoundException, BadRequestException

class CommuneService:
    def __init__(self, db: Session):
        self.repo = CommuneRepository(db)
        self.departement_repo = DepartementRepository(db)  # Placeholder for DepartementRepository if needed

    # ------------------------
    # LIST ALL
    # ------------------------
    def list_communes(self) -> List[CommuneRead]:
        return self.repo.get_list_communes()

    # ------------------------
    # PAGINATION
    # ------------------------
    def list_communes_paginated(self, limit: int, offset: int) -> Dict[str, Any]:
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
    def get_commune(self, idcommune: int) -> Commune:
        obj = self.repo.get_by_id(idcommune)
        if not obj:
            raise NotFoundException(f"Commune {idcommune} introuvable")
        return obj

    # ------------------------
    # CREATE
    # ------------------------
    def create_commune(self, data: CommuneBase) -> Commune:
        try:
            obj = Commune(**data.model_dump())
            departement =  self.departement_repo.get_by_id(data.id_departement) if data.id_departement else None
            if data.id_departement and not departement:
                raise NotFoundException(f"Département {data.id_departement} introuvable")
            return self.repo.create(obj)
        except Exception as e:
            raise BadRequestException(str(e))

    # ------------------------
    # UPDATE / PATCH
    # ------------------------
    def update_commune(self, idcommune: int, data: CommunePatch) -> Commune:
        obj = self.get_commune(idcommune)
        departement =  self.departement_repo.get_by_id(data.id_departement) if data.id_departement else None
        if data.id_departement and not departement:
            raise NotFoundException(f"Département {data.id_departement} introuvable")

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
    def delete_commune(self, idcommune: int) -> None:
        obj = self.get_commune(idcommune)
        try:
            self.repo.delete(obj)
        except Exception as e:
            raise BadRequestException(str(e))
