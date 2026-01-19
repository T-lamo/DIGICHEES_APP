from typing import List, Optional
from sqlmodel import SQLModel, Field
from decimal import Decimal
from datetime import date



class UtilisateurBase(SQLModel):
    nom_utilisateur: str | None = Field(default=None, max_length=50)
    prenom_utilisateur: str | None = Field(default=None, max_length=50)
    username: str | None = Field(default=None, max_length=50)
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
    password: str
    roles_ids: List[int] = [] 



class UtilisateurRead(UtilisateurBase):
    id: int
    roles_ids: List[int] = [] 



__all__ = ["UtilisateurBase", "UtilisateurRead", "UtilisateurPatch", "UtilisateurCreate"]