from datetime import datetime
from sqlalchemy import CheckConstraint, Boolean, String, DateTime, ForeignKey, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class Vehiculo(Base):
    __tablename__ = "vehiculos"
    
    __table_args__ = (
        CheckConstraint("tipo IN ('AUTO', 'BUS', 'CAMION', 'MOTOCICLIO', 'PICK-UP')", name="tipo_check"),
    )
    
    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    placa: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    marca: Mapped[str | None] = mapped_column(String(50), nullable=True)
    modelo: Mapped[str | None] = mapped_column(String(50), nullable=True)
    color: Mapped[str | None] = mapped_column(String(30), nullable=True)
    estado: Mapped[bool] = mapped_column(Boolean, default="ACTIVO", nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id", ondelete="CASCADE", onupdate="RESTRICT"), nullable=False)
    
    cliente = relationship("Cliente", back_populates="vehiculos")
    
    movimientos = relationship("Movimiento", back_populates="vehiculo")