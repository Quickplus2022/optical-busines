from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey, Date, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    
    # Dados básicos
    name = Column(String(200), nullable=False)
    contact_person = Column(String(100))
    email = Column(String(255))
    phone = Column(String(20))
    cnpj_cpf = Column(String(18))
    
    # Endereço
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(50))
    postal_code = Column(String(10))
    
    # Informações comerciais
    payment_terms = Column(Integer)  # dias
    delivery_time = Column(Integer)  # dias
    minimum_order = Column(Numeric(12, 2))
    
    # Avaliação
    rating = Column(Numeric(3, 2))
    notes = Column(Text)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Constraints
    __table_args__ = (
        CheckConstraint('rating >= 0 AND rating <= 5', name='check_rating_range'),
    )
    
    # Relacionamentos
    business = relationship("Business", back_populates="suppliers")
    supplier_prices = relationship("SupplierPrice", back_populates="supplier", cascade="all, delete-orphan")


class ProductService(Base):
    __tablename__ = "products_services"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    
    # Dados básicos
    name = Column(String(200), nullable=False)
    description = Column(Text)
    type = Column(String(20), nullable=False)  # product, service
    category = Column(String(100))
    unit = Column(String(20), nullable=False)  # unidade, kg, hora, m², etc.
    
    # Preços
    base_cost = Column(Numeric(12, 2), nullable=False)
    markup_percentage = Column(Numeric(5, 2), default=0.00)
    sale_price = Column(Numeric(12, 2), nullable=False)
    
    # Impostos
    tax_percentage = Column(Numeric(5, 2), default=0.00)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Constraints
    __table_args__ = (
        CheckConstraint("type IN ('product', 'service')", name='check_product_service_type'),
    )
    
    # Relacionamentos
    business = relationship("Business", back_populates="products_services")
    supplier_prices = relationship("SupplierPrice", back_populates="product_service", cascade="all, delete-orphan")
    variable_costs = relationship("VariableCost", back_populates="product_service")


class SupplierPrice(Base):
    __tablename__ = "supplier_prices"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id", ondelete="CASCADE"), nullable=False)
    product_service_id = Column(UUID(as_uuid=True), ForeignKey("products_services.id", ondelete="CASCADE"), nullable=False)
    
    # Preço e período
    price = Column(Numeric(12, 2), nullable=False)
    effective_date = Column(Date, nullable=False)
    end_date = Column(Date)
    notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    supplier = relationship("Supplier", back_populates="supplier_prices")
    product_service = relationship("ProductService", back_populates="supplier_prices")