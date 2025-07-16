from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime, date
import uuid


class BusinessBase(BaseModel):
    name: str
    description: Optional[str] = None
    segment: str
    industry: str
    business_type: str  # MEI, Ltda, SA, etc.
    cnpj: Optional[str] = None
    founded_date: Optional[date] = None
    
    # Localização
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: str = "Brasil"
    
    # Público-alvo
    target_audience: Optional[str] = None
    market_size: Optional[str] = None
    
    @validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('Nome do negócio deve ter pelo menos 3 caracteres')
        return v.strip()
    
    @validator('cnpj')
    def validate_cnpj(cls, v):
        if v:
            # Remove formatação
            cnpj = ''.join(filter(str.isdigit, v))
            if len(cnpj) != 14:
                raise ValueError('CNPJ deve ter 14 dígitos')
            return cnpj
        return v


class BusinessCreate(BusinessBase):
    pass


class BusinessUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    segment: Optional[str] = None
    industry: Optional[str] = None
    business_type: Optional[str] = None
    cnpj: Optional[str] = None
    founded_date: Optional[date] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    target_audience: Optional[str] = None
    market_size: Optional[str] = None
    
    @validator('name')
    def validate_name(cls, v):
        if v is not None and (not v or len(v.strip()) < 3):
            raise ValueError('Nome do negócio deve ter pelo menos 3 caracteres')
        return v.strip() if v else v


class BusinessResponse(BusinessBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True