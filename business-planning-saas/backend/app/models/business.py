from sqlalchemy import Column, String, Text, Date, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.database import Base


class Business(Base):
    __tablename__ = "businesses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Dados básicos
    name = Column(String(200), nullable=False)
    description = Column(Text)
    segment = Column(String(100), nullable=False)
    industry = Column(String(100), nullable=False)
    business_type = Column(String(50), nullable=False)  # MEI, Ltda, SA, etc.
    cnpj = Column(String(18), unique=True)
    founded_date = Column(Date)
    
    # Localização
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(50))
    postal_code = Column(String(10))
    country = Column(String(50), default="Brasil")
    
    # Público-alvo
    target_audience = Column(Text)
    market_size = Column(String(50))
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    owner = relationship("User", back_populates="businesses")
    suppliers = relationship("Supplier", back_populates="business", cascade="all, delete-orphan")
    products_services = relationship("ProductService", back_populates="business", cascade="all, delete-orphan")
    fixed_costs = relationship("FixedCost", back_populates="business", cascade="all, delete-orphan")
    variable_costs = relationship("VariableCost", back_populates="business", cascade="all, delete-orphan")
    financial_projections = relationship("FinancialProjection", back_populates="business", cascade="all, delete-orphan")
    dre_statements = relationship("DREStatement", back_populates="business", cascade="all, delete-orphan")
    swot_analyses = relationship("SWOTAnalysis", back_populates="business", cascade="all, delete-orphan")
    business_canvases = relationship("BusinessCanvas", back_populates="business", cascade="all, delete-orphan")
    goals_objectives = relationship("GoalObjective", back_populates="business", cascade="all, delete-orphan")
    kpis = relationship("KPI", back_populates="business", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="business", cascade="all, delete-orphan")