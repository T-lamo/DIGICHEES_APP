from typing import List, Optional
from src.models.role_model import RoleRead
from sqlmodel import SQLModel, Field
from decimal import Decimal
from datetime import date
from src.models.role_model import RoleRead



class UtilisateurBase(SQLModel):
    nom_utilisateur: str  = Field(min_length=2, max_length=50)
    prenom_utilisateur: str  = Field(min_length=2,max_length=50)
    couleur_fond_utilisateur: int = Field(default=0)
    date_insc_utilisateur: date | None = Field(default=None)
    disabled: bool = Field(default=False)



class UtilisateurPatch(UtilisateurBase):
    nom_utilisateur: Optional[str] = None
    prenom_utilisateur: Optional[str] = None
    roles_ids: Optional[List[int]] = None
    date_insc_utilisateur: date | None = None
    disabled: Optional[bool] = None


class UtilisateurCreate(UtilisateurBase):
    username: str  = Field(min_length=2,max_length=50,unique=True)
    password: str
    roles_ids: List[int] = []



class UtilisateurRead(UtilisateurBase):
    id: int
    username: str
    roles_ids: List[int] = []
    roles: List[RoleRead] = []


__all__ = ["UtilisateurBase", "UtilisateurRead", "UtilisateurPatch", "UtilisateurCreate"]

