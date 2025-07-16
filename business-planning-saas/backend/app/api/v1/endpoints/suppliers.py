from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_suppliers():
    """Listar fornecedores - TODO: Implementar"""
    return {"message": "Endpoint de fornecedores em desenvolvimento"}

@router.post("/")
def create_supplier():
    """Criar fornecedor - TODO: Implementar"""
    return {"message": "Endpoint de criação de fornecedor em desenvolvimento"}