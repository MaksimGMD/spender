from fastapi import APIRouter

from app.api.endpoints import users, auth, category, goal, account, transaction


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/user", tags=["User"])
api_router.include_router(account.router, prefix="/account", tags=["Account"])
api_router.include_router(category.router, prefix="/category", tags=["Category"])
api_router.include_router(
    transaction.router, prefix="/transaction", tags=["Transaction"]
)
api_router.include_router(goal.router, prefix="/goal", tags=["Goal"])
