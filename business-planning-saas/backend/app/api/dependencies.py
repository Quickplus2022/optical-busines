from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.security import verify_token
from app.db.database import get_db
from app.models.user import User
from app.models.business import Business

# Configurar o esquema de autenticação
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Dependency para obter o usuário atual autenticado"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Verificar o token
        payload = verify_token(credentials.credentials)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    
    # Buscar o usuário no banco de dados
    user = db.query(User).filter(User.id == user_id).first()
    if user is None or not user.is_active:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Dependency para obter usuário ativo"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    return current_user


def get_user_business(business_id: str):
    """Factory para criar dependency que verifica se o negócio pertence ao usuário"""
    async def _get_user_business(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ) -> Business:
        """Verificar se o negócio pertence ao usuário atual"""
        business = db.query(Business).filter(
            Business.id == business_id,
            Business.owner_id == current_user.id,
            Business.is_active == True
        ).first()
        
        if not business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Negócio não encontrado ou você não tem permissão para acessá-lo"
            )
        
        return business
    
    return _get_user_business


async def get_business_by_id(
    business_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Business:
    """Dependency para obter um negócio específico do usuário"""
    business = db.query(Business).filter(
        Business.id == business_id,
        Business.owner_id == current_user.id,
        Business.is_active == True
    ).first()
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Negócio não encontrado"
        )
    
    return business