from typing import Any, Dict, List
from sqlmodel import Session
from src.repositories.utilisateur_repository import UtilisateurRepository
from src.models import Utilisateur, UtilisateurBase, UtilisateurRead, UtilisateurPatch, UtilisateurCreate
from src.core import NotFoundException, BadRequestException
from src.core.auth.security import get_password_hash
from src.repositories.role_repository import RoleRepository

class UtilisateurService:
    def __init__(self, db: Session):
        self.repo = UtilisateurRepository(db)
        self.role_repo = RoleRepository(db)


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
        # Remove passwords from the returned data
        items_read = [UtilisateurRead.from_orm(user) for user in items]
        total = self.repo.count()

        return {
            "limit": limit,
            "offset": offset,
            "total": total,
            "data": items_read
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
            # On vérifie si c'est vide, None, ou si l'utilisateur a laissé le texte "string" de Swagger
            champs_a_verifier = {
            "nom_utilisateur": data.nom_utilisateur,
            "prenom_utilisateur": data.prenom_utilisateur,
            "username": data.username,
            "password": data.password
        }

            for nom_champ, valeur in champs_a_verifier.items():
                if not valeur or valeur.strip() == "":
                    raise BadRequestException(
                        f"Le champ '{nom_champ}' est obligatoire et ne peut pas être vide."
                    )
                if len(data.password) < 6:
                    raise BadRequestException("Le mot de passe doit contenir au moins 6 caractères.")
            
                # 1. Validation : INTERDIRE VIDE (Liste vide ou None)
                if not data.roles_ids or len(data.roles_ids) == 0:
                    raise BadRequestException(
                        "Un utilisateur doit avoir au moins un rôle. La liste ne peut pas être vide. "
                        "Choisissez : 1 (Admin), 2 (Operateur_colis), 3 (Operateur_stock)."
                    )
                
            # 2. Validation : Validation des Rôles : Vérification des IDs
            for r_id in data.roles_ids:
                    if r_id == 0:
                        raise BadRequestException(
                            "Le rôle ne peut pas être 0. "
                            "Choisissez parmi les IDs valides : 1 (Admin), 2 (Operateur_colis), 3 (Operateur_stock)."
                        )
                    
                    # Vérifier si l'ID existe en base (1, 2 ou 3 uniquement)
                    role_obj = self.role_repo.get_by_id(r_id)
                    if not role_obj:
                        raise NotFoundException(
                            f"L'ID de rôle {r_id} n'existe pas. Seuls les IDs 1, 2 et 3 sont autorisés."
                        )

                
             #Création et Hachage du mot de passe   
            obj = Utilisateur(
                **data.model_dump(exclude={"roles_ids", "password"}),
                password=get_password_hash(data.password)
                )
            return self.repo.create_with_roles(obj, data.roles_ids)

        except (BadRequestException, NotFoundException) as e:
            raise e
        except Exception as e:
            raise BadRequestException(f"Erreur lors de la création : {str(e)}")

    # ------------------------
    # UPDATE / PATCH
    # ------------------------
    def update_utilisateur(self, idutilisateur: int, data: UtilisateurPatch) -> Utilisateur:
        obj = self.get_utilisateur(idutilisateur)

        if data.roles_ids is not None:  
        # A. Validation : INTERDIRE VIDE
            if len(data.roles_ids) == 0:
                raise BadRequestException(
                    "La liste des rôles ne peut pas être vide. L'utilisateur doit conserver au moins un rôle."
                )

            # B. Validation : INTERDIRE 0 et IDs inconnus
            for r_id in data.roles_ids:
                if r_id == 0:
                    raise BadRequestException(
                        "Le rôle ne peut pas être 0. Choisissez : 1 (Admin), 2 (Operateur_colis), 3 (Operateur_stock)."
                    )
                
                # Vérification de l'existence en base
                role_obj = self.role_repo.get_by_id(r_id)
                if not role_obj:
                    raise NotFoundException(f"L'ID de rôle {r_id} n'existe pas dans le système.")

            # C. Mise à jour de la relation (Table de liaison)
            # On appelle la méthode du repository pour synchroniser t_utilisateur_role
            self.repo.update_roles(idutilisateur, data.roles_ids)

        # 3. Mise à jour des autres champs (username, etc.)
        update_data = data.model_dump(exclude_unset=True, exclude={"roles_ids"})
        for key, value in update_data.items():
            setattr(obj, key, value)

        try:
            return self.repo.update(obj)
        except Exception as e:
            raise BadRequestException(f"Erreur lors de la mise à jour : {str(e)}")   

    # ------------------------
    # DELETE
    # ------------------------
    def delete_utilisateur(self, idutilisateur: int) -> None:
        obj = self.get_utilisateur(idutilisateur)
        try:
            self.repo.delete(obj)
        except Exception as e:
            raise BadRequestException(str(e))