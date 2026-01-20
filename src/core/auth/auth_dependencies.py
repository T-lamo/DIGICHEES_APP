from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from src.conf.db.database import Database
from src.core.auth.auth_service import AuthService
from src.models import Utilisateur
from src.settings import settings
from jose import JWTError, jwt

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

## get current token for active user
def get_current_active_user(
    db: Session = Depends(Database.get_session),
    token: str = Depends(oauth2_scheme)
) -> Utilisateur:
    service = AuthService(db)
    return service.get_current_active_user(token)

def get_user_sub_from_token(token: str) -> str | None:
    """
    Extracts the 'sub' claim from a JWT token.
    Returns None if the token is invalid.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        sub = payload.get("sub")
        return sub
    except JWTError:
        return None

# def require_admin(user: Utilisateur = Depends(get_current_active_user)):
#     if user.role != "admin":
#         raise HTTPException(status_code=403, detail="Admins only")
#     return user