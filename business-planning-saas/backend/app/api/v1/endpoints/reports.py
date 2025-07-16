from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_reports():
    """Listar relatórios - TODO: Implementar"""
    return {"message": "Endpoint de relatórios em desenvolvimento"}

@router.post("/generate")
def generate_report():
    """Gerar relatório - TODO: Implementar"""
    return {"message": "Endpoint de geração de relatório em desenvolvimento"}