from typing import List, Optional
from sqlmodel import SQLModel, Field
from decimal import Decimal
from enum import Enum

class RoleName(str, Enum):
    ADMIN = "Admin"
    OPERATEUR_COLIS = "Operateur colis"
    OPERATEUR_STOCK = "Operateur Stock"

class RoleBase(SQLModel):
    #librole: str = Field(index=True, unique=True)
    librole: RoleName = Field(unique=True, nullable=False)

class RolePatch(RoleBase):
    librole: Optional[RoleName] = None

class RoleRead(RoleBase):
    codrole: int

__all__ = ["RoleBase", "RoleRead", "RolePatch", "RoleName"]


