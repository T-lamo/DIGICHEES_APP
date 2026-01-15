from typing import List, Optional
from sqlmodel import SQLModel, Field

class Poids(SQLModel, table=True):
    """Table représentant les poids et timbres associés aux commandes."""
    
    __tablename__ = "t_poids"
    
    id: int | None = Field(default=None, primary_key=True)
    valmin: Decimal | None = Field(default=Decimal("0"), nullable=True)
    valtimbre: Decimal | None = Field(default=Decimal("0"), nullable=True)