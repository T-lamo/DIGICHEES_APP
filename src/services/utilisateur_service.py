from typing import Any, Dict, List
from sqlmodel import Session
from src.repositories.utilisateur_repository import UtilisateurRepository
from src.models import Utilisateur, UtilisateurBase, UtilisateurRead, UtilisateurPatch, UtilisateurCreate
from src.core import NotFoundException, BadRequestException
from src.core.auth.security import get_password_hash

class UtilisateurService:
    def __init__(self, db: Session):
        self.repo = UtilisateurRepository(db)


    # ------------------------
    # LIST ALL
    # ------------------------
    def list_utilisateur(self) -> List[UtilisateurRead]:
        return self.repo.get_list_utilisateurs()

    # ------------------------
    # PAGINATION
    # ------------------------
    def list_utilisateurs(
        self, limit: int, offset: int
    ) -> Dict[str, Any]:
        items = self.repo.get_paginated(limit, offset)
        total = self.repo.count()

        return {
            "limit": limit,
            "offset": offset,
            "total": total,
            "data": items
        }

# ------------------------
    # GET BY ID
    # ------------------------
    def get_utilisateur(self, idutilisateur: int) -> Utilisateur:
        obj = self.repo.get_by_id(idutilisateur)
        if not obj:
            raise NotFoundException(f"Utilisateur {idutilisateur} introuvable")
        return obj


# ------------------------
    # CREATE
    # ------------------------
    #def create_utilisateur(
    #    self, data: UtilisateurBase
    #) -> Utilisateur:
    #    try:
    #        obj = Utilisateur(**data.model_dump())
    #        return self.repo.create(obj)
    #    except Exception as e:
    #        raise BadRequestException(str(e))
    
    def create_utilisateur(self, data: UtilisateurCreate) -> Utilisateur:
        try:
            #  On extrait les rôles et on exclut le champ du modèle DB
            roles_a_ajouter = data.roles_ids

            # On hash le mot de passe s’il existe
            hashed_password = None
            if data.password:
                hashed_password = get_password_hash(data.password)

            # On crée l'objet Utilisateur sans le champ roles_ids
            obj = Utilisateur(
                **data.model_dump(exclude={"roles_ids", "password"}),
                password=hashed_password
            )
            
            # On utilise la nouvelle méthode du repo
            return self.repo.create_with_roles(obj, roles_a_ajouter)
        except Exception as e:
            raise BadRequestException(str(e))


    # ------------------------
    # UPDATE / PATCH
    # ------------------------
    def update_utilisateur(self, idutilisateur: int, data: UtilisateurPatch) -> Utilisateur:
        obj = self.get_utilisateur(idutilisateur)

        # 2. TRAITEMENT SPÉCIAL POUR LES RÔLES
        if data.roles_ids is not None:
            self.repo.update_roles(idutilisateur, data.roles_ids)

        #  On exclut "roles_ids" de la boucle setattr
        # Sinon, SQLModel plante car il ne trouve pas cette colonne en base
        update_data = data.model_dump(exclude_unset=True, exclude={"roles_ids"})
        
        for key, value in update_data.items():
            setattr(obj, key, value)

        try:
            return self.repo.update(obj)
        except Exception as e:
            raise BadRequestException(str(e))

    # ------------------------
    # DELETE
    # ------------------------
    def delete_utilisateur(self, idutilisateur: int) -> None:
        obj = self.get_utilisateur(idutilisateur)
        try:
            self.repo.delete(obj)
        except Exception as e:
            raise BadRequestException(str(e))