from .v1 import router as auth_router
from .settings import router as settings_router

__all__ = ["auth_router", "settings_router"]
