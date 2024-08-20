from fastapi import APIRouter

from .login import login_router
from .read import read_router
from .write import write_router

api_router = APIRouter(prefix='/api')
api_router.include_router(read_router)
api_router.include_router(login_router)
api_router.include_router(write_router)
