from typing import List, Optional
from sqlmodel import SQLModel, Field
from decimal import Decimal



class PoidsBase(SQLModel):
    libpoids: str | None = Field(default=None, max_length=50, nullable=True)
    poidspoids: int | None = Field(default=None, nullable=True)
    prixcond: Decimal = Field(default=Decimal("0.0000"), nullable=False)
    ordreimp: int | None = Field(default=None, nullable=True)
    

class PoidsPatch(PoidsBase):
    prixcond: Decimal | None = None


class PoidsRead(PoidsBase):
    idpoids: int

__all__ = ["PoidsBase", "PoidsRead", "PoidsPatch"]