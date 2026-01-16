from .exemple_route import router as exemple_router  
from .conditionnement_route import router as conditionnement_router
from .objet_route import router as objet_router
from .vignette_route import router as vignette_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(exemple_router)
router.include_router(conditionnement_router)   
router.include_router(vignette_router)   
router.include_router(objet_router)


__all__ = ["router"]