from typing import List, Optional
from sqlmodel import SQLModel, Field
from decimal import Decimal



class ConditionnementBase(SQLModel):
    libelle: str | None = Field(default=None, max_length=50, nullable=True)
    poids: int | None = Field(default=None, nullable=True)
    prix: Decimal = Field(default=Decimal("0.0000"), nullable=False)
    ordreimp: int | None = Field(default=None, nullable=True)
    

class ConditionnementPatch(ConditionnementBase):
    prix: Decimal | None = None


class ConditionnementRead(ConditionnementBase):
    id: int

__all__ = ["ConditionnementBase", "ConditionnementRead", "ConditionnementPatch"]

