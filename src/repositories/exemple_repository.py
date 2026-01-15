from sqlmodel import Session
from src.models.exemple_model import Exemple
class ExempleRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_list_exemple(self):
        """Récupère la liste de tous les exemples."""
        return self.session.query(Exemple).all()