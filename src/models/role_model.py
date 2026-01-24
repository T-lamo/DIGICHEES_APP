from typing import List, Optional
from sqlmodel import SQLModel, Field
from decimal import Decimal
from enum import Enum

class RoleName(str, Enum):
    ADMIN = "Admin"
    OPERATEUR_COLIS = "Operateur_colis"
    OPERATEUR_STOCK = "Operateur_stock"

class RoleBase(SQLModel):
    librole: str = Field(index=True, unique=True)
    #librole: RoleName = Field(unique=True, nullable=False)

class RolePatch(RoleBase):
    librole: Optional[str] = None

class RoleRead(RoleBase):
    id: int

__all__ = ["RoleBase", "RoleRead", "RolePatch", "RoleName"]


