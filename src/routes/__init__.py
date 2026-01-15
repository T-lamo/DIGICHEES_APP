from .exemple_route import router as exemple_router  
from .conditionnement_route import router as conditionnement_router 
from fastapi import APIRouter

router = APIRouter()
router.include_router(exemple_router)
router.include_router(conditionnement_router)   

__all__ = ["router"]