from typing import List, Optional
from sqlmodel import SQLModel, Field
from decimal import Decimal

class PoidsBase(SQLModel):
    min: Decimal | None = Field(default=Decimal("0"), nullable=True)
    value: Decimal | None = Field(default=Decimal("0"), nullable=True)
    

class PoidsPatch(PoidsBase):
    min: Decimal | None = None
    value: Decimal | None = None


class PoidsRead(PoidsBase):
    id: int



__all__ = ["PoidsBase", "PoidsRead", "PoidsPatch"]