from typing import List, Optional
from sqlmodel import SQLModel, Field
from decimal import Decimal



class CommuneBase(SQLModel):
    code_departement: Optional[int] = Field(default=None, nullable=True)
    cp: str | None = Field(default=None, max_length=5)  # code postal
    nom: str | None = Field(default=None, max_length=50)  # nom de la commune
    

class CommunePatch(CommuneBase):
    cp: Optional[str] = None
    nom: Optional[str] = None


class CommuneRead(CommuneBase):
    id: int

__all__ = ["CommuneBase", "CommuneRead", "CommunePatch"]

