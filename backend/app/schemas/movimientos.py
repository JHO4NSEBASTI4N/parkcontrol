from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal

class MovimientoCrear(BaseModel):
    vehiculo_id: int = Field(gt=0)
    usuario_ingreso_id: int | None = Field(gt=0, default=None)
    
    
class MovimientoFinalizar(BaseModel):
    usuario_salida_id: int | None = Field(gt=0, default=None)
    
class MovimientoRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    vehiculo_id: int
    usuario_ingreso_id: int | None
    usuario_salida_id: int | None
    fecha_ingreso: datetime
    fecha_salida: datetime | None
    minutos: int | None
    valor_total: Decimal | None
    estado: str