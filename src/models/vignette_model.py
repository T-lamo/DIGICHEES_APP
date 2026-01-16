
   
from typing import List, Optional
from sqlmodel import SQLModel, Field
from decimal import Decimal


class VignetteBase(SQLModel):
    min: Decimal | None = Field(default=Decimal("0"), nullable=True)
    value: Decimal | None = Field(default=Decimal("0"), nullable=True)

class VignettePatch(VignetteBase):
    min: Decimal | None = None
    value: Decimal | None = None


class VignetteRead(VignetteBase):
    id: int

__all__ = ["VignetteBase", "VignetteRead", "VignettePatch"]

