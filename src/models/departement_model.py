

from typing import List, Optional
from src.models.commune_model import CommuneRead
from sqlmodel import SQLModel, Field
from decimal import Decimal



class DepartementBase(SQLModel):
    code: str = Field(max_length=2, nullable=False, index=True)  # code officiel du département
    nom: str | None = Field(default=None, max_length=50)          # nom du département
    ordre_aff: int = Field(default=0)
    

class DepartementPatch(DepartementBase):
    code: Optional[str] = None
    nom: Optional[str] = None
    ordre_aff: Optional[int] = None


class DepartementRead(DepartementBase):
    id: int
    communes: List[CommuneRead] = []


__all__ = ["DepartementBase", "DepartementRead", "DepartementPatch"]

