from fastapi import APIRouter
from app.api.api_v1.endpoints import home, top_holders

api_router = APIRouter()

api_router.include_router(home.router)
api_router.include_router(top_holders.router)