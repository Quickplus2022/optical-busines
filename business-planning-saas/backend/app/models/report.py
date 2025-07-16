from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.database import Base


class Report(Base):
    __tablename__ = "reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Dados do relatório
    name = Column(String(200), nullable=False)
    type = Column(String(50), nullable=False)    # financial, strategic, complete, custom
    format = Column(String(10), nullable=False)  # pdf, excel
    
    # Configuração usada na geração
    config = Column(JSONB)  # Parâmetros específicos do relatório
    
    # Arquivo gerado
    file_path = Column(String(500))
    file_size = Column(Integer)  # bytes
    
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    business = relationship("Business", back_populates="reports")
    user = relationship("User", back_populates="reports")