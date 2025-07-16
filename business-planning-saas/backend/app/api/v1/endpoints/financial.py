from fastapi import APIRouter

router = APIRouter()

@router.get("/projections")
def list_financial_projections():
    """Listar projeções financeiras - TODO: Implementar"""
    return {"message": "Endpoint de projeções financeiras em desenvolvimento"}

@router.post("/projections")
def create_financial_projection():
    """Criar projeção financeira - TODO: Implementar"""
    return {"message": "Endpoint de criação de projeção financeira em desenvolvimento"}

@router.get("/dre")
def list_dre_statements():
    """Listar DREs - TODO: Implementar"""
    return {"message": "Endpoint de DRE em desenvolvimento"}