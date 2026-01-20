from sqlmodel import SQLModel, Field
from decimal import Decimal



class ObjetBase(SQLModel):
    libobj: str | None = Field(default=None, max_length=50, nullable=True)
    tailleobj: str | None = Field(default=None, max_length=50, nullable=True)
    puobj: Decimal = Field(default=Decimal("0.0000"), nullable=False)
    poidsobj: Decimal = Field(default=Decimal("0.0000"), nullable=False)
    indispobj: int = Field(default=0)
    o_imp: int = Field(default=0)
    o_aff: int = Field(default=0)
    o_cartp: int = Field(default=0)
    points: int = Field(default=0)
    o_ordre_aff: int = Field(default=0)
    

class ObjetPatch(ObjetBase):
    pass


class ObjetRead(ObjetBase):
    id: int

__all__ = ["ObjetBase", "ObjetRead", "ObjetPatch"]

