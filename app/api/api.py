from fastapi import APIRouter

from app.api.endpoints import users, auth, category


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/user", tags=["User"])
api_router.include_router(category.router, prefix="/category", tags=["Category"])