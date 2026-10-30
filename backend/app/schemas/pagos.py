from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class PagoCrear(BaseModel):
    movimiento_id: int = Field(gt=0)
    valor: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    metodo_pago: str = Field(pattern=r"^(efectivo|tarjeta|transferencia)$")
    
    
class PagoRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    movimiento_id: int
    valor: Decimal
    metodo_pago: str
    fecha_pago: datetime
    estado: str