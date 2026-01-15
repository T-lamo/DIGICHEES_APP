from .exemple_route import router as exemple_router  
from fastapi import APIRouter

router = APIRouter()
router.include_router(exemple_router)

__all__ = ["router"]