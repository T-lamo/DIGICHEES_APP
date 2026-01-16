from sqlmodel import Session
from src.repositories.exemple_repository import ExempleRepository
class ExempleService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = ExempleRepository(self.session)

    def list_exemple(self):
        """Liste tous les exemples."""
        self.repo.get_list_exemple(self.session)