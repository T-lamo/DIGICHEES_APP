from fastapi import Depends
from fastapi import APIRouter
from src.core.auth.auth_dependencies import require_admin_role
from src.core.auth.auth_route import router as auth_router  
from src.core.auth import get_current_active_user
from .objet_route import router as objet_router
from .vignette_route import router as vignette_router
from .conditionnement_route import router as conditionnement_router 
from .poids_route import router as poids_router 
from .utilisateur_route import private_router as utilisateur_private_router
from .utilisateur_route import public_router as utilisateur_public_router
from .role_route import router as role_router
from .commune_route import router as commune_router
from .departement_route import router as departement_router


router = APIRouter()
router.include_router(auth_router)
router.include_router(utilisateur_private_router, dependencies=[Depends(get_current_active_user), Depends(require_admin_role)])   
router.include_router(role_router, dependencies=[Depends(get_current_active_user), Depends(require_admin_role)])  
router.include_router(conditionnement_router, dependencies=[Depends(get_current_active_user),  Depends(require_admin_role)])   
router.include_router(vignette_router, dependencies=[Depends(get_current_active_user), Depends(require_admin_role)])   
router.include_router(objet_router, dependencies=[Depends(get_current_active_user), Depends(require_admin_role)])
router.include_router(poids_router, dependencies=[Depends(get_current_active_user), Depends(require_admin_role)])   
router.include_router(commune_router, dependencies=[Depends(get_current_active_user), Depends(require_admin_role)])   
router.include_router(departement_router, dependencies=[Depends(get_current_active_user), Depends(require_admin_role)])   
router.include_router(utilisateur_public_router, dependencies=[Depends(get_current_active_user) ,Depends(require_admin_role)])   


__all__ = ["router"]