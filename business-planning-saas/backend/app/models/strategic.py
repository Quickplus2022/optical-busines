from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.types import Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.database import Base


class SWOTAnalysis(Base):
    __tablename__ = "swot_analysis"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    
    # Dados da análise
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Análise SWOT (arrays de strings em JSON)
    strengths = Column(JSONB)      # Forças
    weaknesses = Column(JSONB)     # Fraquezas  
    opportunities = Column(JSONB)  # Oportunidades
    threats = Column(JSONB)        # Ameaças
    
    # Planos de ação derivados da análise
    action_items = Column(JSONB)   # Array de objetos com ações
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    business = relationship("Business", back_populates="swot_analyses")


class BusinessCanvas(Base):
    __tablename__ = "business_canvas"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    
    # Identificação
    name = Column(String(200), nullable=False)
    
    # Os 9 blocos do Business Model Canvas
    key_partners = Column(JSONB)           # Parcerias-chave
    key_activities = Column(JSONB)         # Atividades-chave
    key_resources = Column(JSONB)          # Recursos-chave
    value_propositions = Column(JSONB)     # Propostas de valor
    customer_relationships = Column(JSONB) # Relacionamento com clientes
    channels = Column(JSONB)               # Canais
    customer_segments = Column(JSONB)      # Segmentos de clientes
    cost_structure = Column(JSONB)         # Estrutura de custos
    revenue_streams = Column(JSONB)        # Fontes de receita
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    business = relationship("Business", back_populates="business_canvases")


class GoalObjective(Base):
    __tablename__ = "goals_objectives"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    
    # Dados da meta
    title = Column(String(200), nullable=False)
    description = Column(Text)
    type = Column(String(50), nullable=False)  # financial, operational, strategic, etc.
    
    # SMART Goals
    target_value = Column(Numeric(15, 2))
    current_value = Column(Numeric(15, 2), default=0)
    unit = Column(String(50))  # R$, %, unidades, clientes, etc.
    deadline = Column(Date)
    
    # Status de acompanhamento
    status = Column(String(20), default='active')  # active, completed, cancelled
    progress_percentage = Column(Numeric(5, 2), default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    business = relationship("Business", back_populates="goals_objectives")
    kpis = relationship("KPI", back_populates="goal", cascade="all, delete-orphan")


class KPI(Base):
    __tablename__ = "kpis"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    goal_id = Column(UUID(as_uuid=True), ForeignKey("goals_objectives.id", ondelete="CASCADE"), nullable=False)
    
    # Dados do KPI
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Configuração do KPI
    calculation_method = Column(Text)  # Como calcular o KPI
    frequency = Column(String(20))     # daily, weekly, monthly, quarterly
    target_value = Column(Numeric(15, 2))
    
    # Dados históricos
    historical_data = Column(JSONB)    # [{date: "2024-01", value: 1000}, ...]
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    business = relationship("Business", back_populates="kpis")
    goal = relationship("GoalObjective", back_populates="kpis")