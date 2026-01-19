from typing import List, Optional
from sqlmodel import SQLModel, Field
from decimal import Decimal




class RoleBase(SQLModel):
    librole: str = Field(index=True, unique=True)

class RolePatch(RoleBase):
    librole: Optional[str] = None

class RoleRead(RoleBase):
    codrole: int

__all__ = ["RoleBase", "RoleRead", "RolePatch"]



