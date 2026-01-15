# ------------------------
# Core module - centralisation des exceptions et handlers
# ------------------------

# Import des exceptions
from .exceptions import (
    NotFoundException,
    BadRequestException,
    UnauthorizedException,
    ConflictException,
)

# Import du handler global
from .exceptions_handlers import register_exception_handlers

# Définition explicite de ce qui est exporté
__all__ = [
    "NotFoundException",
    "BadRequestException",
    "UnauthorizedException",
    "ConflictException",
    "register_exception_handlers"
]
