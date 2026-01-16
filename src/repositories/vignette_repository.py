from typing import List, Optional

from sqlmodel import Session, select
from src.models import Vignette, VignetteRead


class VignetteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_list_vignette(self) -> List[VignetteRead]:
        """Récupère la liste de toutes les vignettes."""
        return self.db.query(Vignette).all()

    def get_by_id(self, idvignette: int) -> Optional[Vignette]:
        return self.db.get(Vignette, idvignette)

    def create(self, data: Vignette) -> Vignette:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    def update(self, data: Vignette) -> Vignette:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    def delete(self, data: Vignette) -> None:
        self.db.delete(data)
        self.db.commit()

    def get_paginated(self, limit: int, offset: int) -> List[Vignette]:
        statement = (
            select(Vignette)
            .limit(limit)
            .offset(offset)
        )
        return self.db.exec(statement).all()

    def count(self) -> int:
        statement = select(Vignette)
        return len(self.db.exec(statement).all())
