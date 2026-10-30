from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, String, DateTime, Numeric, Integer, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import FetchedValue

from app.database.base import Base

class Pago(Base):
    __tablename__ = "pagos"
    
    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    movimiento_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), ForeignKey("movimientos.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    valor: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    metodo_pago: Mapped[str] = mapped_column(String(20), nullable=False)
    fecha_pago: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    estado: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("PAGADO"))
    
    movimiento = relationship("Movimiento", back_populates="pago")