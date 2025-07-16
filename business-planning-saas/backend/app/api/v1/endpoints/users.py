from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserUpdate, UserResponse
from app.api.dependencies import get_current_active_user

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_user_profile(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Obter perfil do usuário atual"""
    return current_user


@router.put("/me", response_model=UserResponse)
def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """Atualizar perfil do usuário atual"""
    
    # Atualizar apenas campos fornecidos
    update_data = user_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.delete("/me")
def deactivate_user_account(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """Desativar conta do usuário atual"""
    
    current_user.is_active = False
    db.commit()
    
    return {"message": "Conta desativada com sucesso"}


@router.get("/me/businesses", response_model=List[dict])
def get_user_businesses(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """Obter negócios do usuário atual"""
    
    businesses = []
    for business in current_user.businesses:
        if business.is_active:
            businesses.append({
                "id": business.id,
                "name": business.name,
                "segment": business.segment,
                "industry": business.industry,
                "created_at": business.created_at
            })
    
    return businesses