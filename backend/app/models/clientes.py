from datetime import datetime
from sqlalchemy import Boolean, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class Cliente(Base):
    __tablename__ = "clientes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    documento: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)
    correo: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    estado: Mapped[bool] = mapped_column(Boolean, default="ACTIVO", nullable=False)
    
    vehiculos = relationship("Vehiculo", back_populates="cliente")