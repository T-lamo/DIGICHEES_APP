from typing import List, Optional
from sqlmodel import SQLModel, Field
from decimal import Decimal
from datetime import date



class UtilisateurBase(SQLModel):
    nom_utilisateur: str | None = Field(default=None, max_length=50)
    prenom_utilisateur: str | None = Field(default=None, max_length=50)
    username: str | None = Field(default=None, max_length=50)
    couleur_fond_utilisateur: int = Field(default=0)
    roles_ids: List[int] = [] 

class UtilisateurPatch(SQLModel):
    nom_utilisateur: Optional[str] = None
    prenom_utilisateur: Optional[str] = None
    roles_ids: Optional[List[int]] = None


class UtilisateurRead(UtilisateurBase):
    code_utilisateur: int
    date_insc_utilisateur: Optional[date]


__all__ = ["UtilisateurBase", "UtilisateurRead", "UtilisateurPatch"]