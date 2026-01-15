from typing import List, Optional
from sqlmodel import SQLModel, Field


class ExempleBase(SQLModel):
    name: str

class ExemplePatch(ExempleBase):
    name: Optional[str] = None


class ExempleRead(ExempleBase):
    id: int


class Exemple(ExempleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True)


__all__ = ["Exemple", "ExempleBase", "ExempleRead", "ExemplePatch"]

