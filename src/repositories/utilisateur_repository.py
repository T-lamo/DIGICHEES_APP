from typing import List, Optional

from sqlmodel import Session, select, delete
from src.models import Utilisateur, UtilisateurRead, RoleUtilisateur
from src.models import Role
from sqlalchemy.orm import selectinload

class UtilisateurRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_list_utilisateur(self) -> List[UtilisateurRead]:
        """Récupère la liste de toutes les utilisateurs."""
        #return self.db.query(Utilisateur).all()
        statement = select(Utilisateur).options(selectinload(Utilisateur.roles))
        return self.db.exec(statement).all()

    def get_by_id(self, idutilisateur: int) -> Optional[Utilisateur]:
        #return self.db.get(Utilisateur, idutilisateur)
        statement = select(Utilisateur).where(Utilisateur.id == idutilisateur)
        result = self.db.exec(statement).first()
        return result

    
    def create_with_roles(self, data: Utilisateur, roles_ids: List[int]) -> Utilisateur:
        """Crée l'utilisateur ET ses rôles dans la table de jointure."""
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)

        # Ajout des liens dans t_utilisateur_role
        for r_id in roles_ids:
            lien = RoleUtilisateur(utilisateur_id=data.id, role_id=r_id)
            self.db.add(lien)
        
        self.db.commit()
        self.db.refresh(data)
        return data
    
    def update(self, data: Utilisateur) -> Utilisateur:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data
    
    def update_roles(self, idutilisateur: int, new_roles_ids: List[int]):
        """Supprime les anciens rôles et ajoute les nouveaux."""
        # 1. Supprimer les anciens rôles de cet utilisateur
        statement = delete(RoleUtilisateur).where(RoleUtilisateur.utilisateur_id == idutilisateur)
        self.db.exec(statement)
        
        # 2. Ajouter les nouveaux rôles cochés
        for r_id in new_roles_ids:
            nouveau_lien = RoleUtilisateur(utilisateur_id=idutilisateur, role_id=r_id)
            self.db.add(nouveau_lien)
        
        self.db.commit()

    def delete(self, data: Utilisateur) -> None:
        #"""Supprime l'utilisateur et ses liens de rôles associés"""
        # 1. On supprime d'abord tous les rôles liés à cet utilisateur
        statement = delete(RoleUtilisateur).where(RoleUtilisateur.utilisateur_id == data.id)
        self.db.exec(statement)
        
        # 2. Maintenant on peut supprimer l'utilisateur
        self.db.delete(data)
        
        # 3. On valide la transaction
        self.db.commit()

    def get_paginated(self, limit: int, offset: int) -> List[Utilisateur]:
        statement = (
            select(Utilisateur)
            .options(selectinload(Utilisateur.roles)) # On charge les objets roles
            .limit(limit)
            .offset(offset)
    )
        return self.db.exec(statement).all()

    def count(self) -> int:
        statement = select(Utilisateur)
        return len(self.db.exec(statement).all())