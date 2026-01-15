from typing import List, Optional
from sqlmodel import SQLModel, Field
from decimal import Decimal



class ConditionnementBase(SQLModel):
    libcondit: str | None = Field(default=None, max_length=50, nullable=True)
    poidscondit: int | None = Field(default=None, nullable=True)
    prixcond: Decimal = Field(default=Decimal("0.0000"), nullable=False)
    ordreimp: int | None = Field(default=None, nullable=True)
    

class ConditionnementPatch(ConditionnementBase):
    prixcond: Decimal | None = None


class ConditionnementRead(ConditionnementBase):
    idcondit: int

__all__ = ["ConditionnementBase", "ConditionnementRead", "ConditionnementPatch"]

