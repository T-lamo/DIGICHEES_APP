from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from src.conf.db.database import Database
from src.core.auth.auth_service import AuthService
from src.models import Utilisateur

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

## get current token for active user
def get_current_active_user(
    db: Session = Depends(Database.get_session),
    token: str = Depends(oauth2_scheme)
) -> Utilisateur:
    service = AuthService(db)
    return service.get_current_active_user(token)
