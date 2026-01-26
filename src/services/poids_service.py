from typing import Any, Dict, List
from sqlmodel import Session
from src.repositories.poids_repository import PoidsRepository
from src.models import PoidsRead, Poids, PoidsBase, PoidsPatch
from src.core import NotFoundException, BadRequestException


class PoidsService:
    def __init__(self, db: Session):
        self.repo = PoidsRepository(db)

    # ------------------------
    # LIST ALL
    # ------------------------
    def list_poids(self) -> List[PoidsRead]:
        return self.repo.get_list_poids()

    # ------------------------
    # PAGINATION
    # ------------------------
    def list_poidss(
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
    def get_poids(self, idpoids: int) -> Poids:
        obj = self.repo.get_by_id(idpoids)
        if not obj:
            raise NotFoundException(f"Poids {idpoids} introuvable")
        return obj

    # ------------------------
    # CREATE
    # ------------------------
    def create_poids(
        self, data: PoidsBase
    ) -> Poids:
        # try:
        #     obj = Poids(**data.model_dump())
        #     return self.repo.create(obj)
        # except Exception as e:
        #     # Exemple : violation de contrainte unique ou autre erreur DB
        #     raise BadRequestException(str(e))
        # RÈGLE MÉTIER : Interdire les chiffres inférieurs à 0
        if data.value < 0 or data.min < 0:
            raise BadRequestException("Les valeurs de poids (val/min) ne peuvent pas être négatives.")
            
        try:
            obj = Poids(**data.model_dump())
            return self.repo.create(obj)
        except Exception as e:
            raise BadRequestException(str(e))

    # ------------------------
    # UPDATE / PATCH
    # ------------------------
    def update_poids(
        self, idpoids: int, data: PoidsPatch
    ) -> Poids:
        obj = self.get_poids(idpoids)

        # update_data = data.model_dump(exclude_unset=True)
        # for key, value in update_data.items():
        #     setattr(obj, key, value)

        # try:
        #     return self.repo.update(obj)
        # except Exception as e:
        #     raise BadRequestException(str(e))
        # RÈGLE MÉTIER : Vérifier la valeur si elle est présente dans le patch
        if (data.value is not None and data.value < 0) or (data.min is not None and data.min < 0):
            raise BadRequestException("Modification refusée : les valeurs ne peuvent pas être négatives.")

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
    def delete_poids(self, idpoids: int) -> None:
        obj = self.get_poids(idpoids)
        try:
            self.repo.delete(obj)
        except Exception as e:
            raise BadRequestException(str(e))