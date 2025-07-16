from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.types import Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.database import Base


class FixedCost(Base):
    __tablename__ = "fixed_costs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    
    # Dados do custo
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(100))  # Aluguel, Salários, Software, etc.
    amount = Column(Numeric(12, 2), nullable=False)
    frequency = Column(String(20), nullable=False)  # monthly, quarterly, yearly
    
    # Período de vigência
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    business = relationship("Business", back_populates="fixed_costs")


class VariableCost(Base):
    __tablename__ = "variable_costs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    product_service_id = Column(UUID(as_uuid=True), ForeignKey("products_services.id"), nullable=True)
    
    # Dados do custo
    name = Column(String(200), nullable=False)
    description = Column(Text)
    cost_per_unit = Column(Numeric(12, 2), nullable=False)
    percentage_of_revenue = Column(Numeric(5, 2))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    business = relationship("Business", back_populates="variable_costs")
    product_service = relationship("ProductService", back_populates="variable_costs")


class FinancialProjection(Base):
    __tablename__ = "financial_projections"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    
    # Dados da projeção
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Período da projeção
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # Projeções mensais (JSON para flexibilidade)
    monthly_revenue = Column(JSONB)  # [{month: 1, revenue: 10000}, ...]
    monthly_costs = Column(JSONB)
    monthly_profit = Column(JSONB)
    
    # Métricas calculadas
    break_even_point = Column(Integer)  # mês
    payback_period = Column(Integer)  # meses
    roi_percentage = Column(Numeric(5, 2))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    business = relationship("Business", back_populates="financial_projections")


class DREStatement(Base):
    __tablename__ = "dre_statements"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    
    # Período
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    
    # Receitas
    gross_revenue = Column(Numeric(15, 2), nullable=False)
    taxes_on_sales = Column(Numeric(15, 2), default=0)
    net_revenue = Column(Numeric(15, 2), nullable=False)
    
    # Custos
    direct_costs = Column(Numeric(15, 2), default=0)
    gross_profit = Column(Numeric(15, 2), nullable=False)
    
    # Despesas
    operational_expenses = Column(Numeric(15, 2), default=0)
    administrative_expenses = Column(Numeric(15, 2), default=0)
    selling_expenses = Column(Numeric(15, 2), default=0)
    
    # Resultado
    ebitda = Column(Numeric(15, 2), nullable=False)
    depreciation = Column(Numeric(15, 2), default=0)
    ebit = Column(Numeric(15, 2), nullable=False)
    financial_result = Column(Numeric(15, 2), default=0)
    net_income = Column(Numeric(15, 2), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    business = relationship("Business", back_populates="dre_statements")