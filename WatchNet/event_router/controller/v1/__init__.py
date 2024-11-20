from fastapi import APIRouter
from .interrupt_controller import router as interrupt_router
from .user_controller import router as user_router

v1_router = APIRouter(prefix="/v1", tags=["v1"])

v1_router.include_router(interrupt_router)
v1_router.include_router(user_router)

