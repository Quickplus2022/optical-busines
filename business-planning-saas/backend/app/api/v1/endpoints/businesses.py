from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.database import get_db
from app.models.user import User
from app.models.business import Business
from app.schemas.business import BusinessCreate, BusinessUpdate, BusinessResponse
from app.api.dependencies import get_current_active_user, get_business_by_id

router = APIRouter()


@router.post("/", response_model=BusinessResponse, status_code=status.HTTP_201_CREATED)
def create_business(
    business_data: BusinessCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """Criar novo negócio"""
    
    # Verificar se CNPJ já existe (se fornecido)
    if business_data.cnpj:
        existing_business = db.query(Business).filter(Business.cnpj == business_data.cnpj).first()
        if existing_business:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CNPJ já está em uso"
            )
    
    # Criar negócio
    business = Business(
        owner_id=current_user.id,
        **business_data.dict()
    )
    
    db.add(business)
    db.commit()
    db.refresh(business)
    
    return business


@router.get("/", response_model=List[BusinessResponse])
def list_businesses(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
) -> Any:
    """Listar negócios do usuário"""
    
    businesses = db.query(Business).filter(
        Business.owner_id == current_user.id,
        Business.is_active == True
    ).offset(skip).limit(limit).all()
    
    return businesses


@router.get("/{business_id}", response_model=BusinessResponse)
def get_business(
    business: Business = Depends(get_business_by_id)
) -> Any:
    """Obter detalhes de um negócio específico"""
    return business


@router.put("/{business_id}", response_model=BusinessResponse)
def update_business(
    business_update: BusinessUpdate,
    business: Business = Depends(get_business_by_id),
    db: Session = Depends(get_db)
) -> Any:
    """Atualizar negócio"""
    
    # Verificar CNPJ único se estiver sendo alterado
    if business_update.cnpj and business_update.cnpj != business.cnpj:
        existing_business = db.query(Business).filter(
            Business.cnpj == business_update.cnpj,
            Business.id != business.id
        ).first()
        if existing_business:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CNPJ já está em uso"
            )
    
    # Atualizar campos
    update_data = business_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(business, field, value)
    
    db.commit()
    db.refresh(business)
    
    return business


@router.delete("/{business_id}")
def delete_business(
    business: Business = Depends(get_business_by_id),
    db: Session = Depends(get_db)
) -> Any:
    """Excluir negócio (soft delete)"""
    
    business.is_active = False
    db.commit()
    
    return {"message": "Negócio excluído com sucesso"}


@router.get("/{business_id}/dashboard")
def get_business_dashboard(
    business: Business = Depends(get_business_by_id),
    db: Session = Depends(get_db)
) -> Any:
    """Obter dados do dashboard do negócio"""
    
    # Contadores básicos
    suppliers_count = len([s for s in business.suppliers if s.is_active])
    products_services_count = len([p for p in business.products_services if p.is_active])
    fixed_costs_count = len([f for f in business.fixed_costs if f.is_active])
    projections_count = len(business.financial_projections)
    
    # Últimas atividades (últimos DREs, projeções, etc.)
    latest_dre = None
    if business.dre_statements:
        latest_dre = max(business.dre_statements, key=lambda x: x.created_at)
    
    latest_projection = None
    if business.financial_projections:
        latest_projection = max(business.financial_projections, key=lambda x: x.created_at)
    
    return {
        "business_id": business.id,
        "business_name": business.name,
        "counters": {
            "suppliers": suppliers_count,
            "products_services": products_services_count,
            "fixed_costs": fixed_costs_count,
            "projections": projections_count,
            "swot_analyses": len(business.swot_analyses),
            "canvases": len(business.business_canvases),
            "goals": len(business.goals_objectives)
        },
        "latest_dre": {
            "id": latest_dre.id,
            "period_start": latest_dre.period_start,
            "period_end": latest_dre.period_end,
            "net_income": float(latest_dre.net_income)
        } if latest_dre else None,
        "latest_projection": {
            "id": latest_projection.id,
            "name": latest_projection.name,
            "start_date": latest_projection.start_date,
            "end_date": latest_projection.end_date,
            "roi_percentage": float(latest_projection.roi_percentage) if latest_projection.roi_percentage else None
        } if latest_projection else None
    }