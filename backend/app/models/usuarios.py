from datetime import datetime
from sqlalchemy import Boolean, Integer, String, DateTime, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    correo: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[str] = mapped_column(String(20), default="OPERADOR", nullable=False)
    estado: Mapped[bool] = mapped_column(Boolean, default="ACTIVO", nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, nullable=False , server_default=text("CURRENT_TIMESTAMP"))
    fecha_ultima_actualizacion: Mapped[datetime] = mapped_column(DateTime, nullable=False , server_default=text("CURRENT_TIMESTAMP"), server_onupdate=FetchedValue())
    
    movimientos_ingreso = relationship("Movimiento", back_populates="usuario_ingreso", foreign_keys="[Movimiento.usuario_ingreso_id]")
    movimientos_salida = relationship("Movimiento", back_populates="usuario_salida", foreign_keys="[Movimiento.usuario_salida_id]")