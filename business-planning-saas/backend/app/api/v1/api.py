from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, businesses, suppliers, financial, strategic, reports

api_router = APIRouter()

# Incluir todas as rotas
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(businesses.router, prefix="/businesses", tags=["businesses"])
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["suppliers"])
api_router.include_router(financial.router, prefix="/financial", tags=["financial"])
api_router.include_router(strategic.router, prefix="/strategic", tags=["strategic"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])