from fastapi import APIRouter

from app.api.endpoints.categories import router as categories_router
from app.api.endpoints.products import router as products_router
from app.api.endpoints.transactions import router as transactions_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(categories_router)
api_router.include_router(products_router)
api_router.include_router(transactions_router)
