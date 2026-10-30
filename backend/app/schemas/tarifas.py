from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class TarifaBase(BaseModel):
    tipo_vehiculo: str = Field(pattern=r"^(bicicleta|moto|patineta)$")
    valor_minimo: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    
class TarifaCrear(TarifaBase):
    pass

class TarifaActualizar(BaseModel):
    tipo_vehiculo: str | None = Field(default=None, pattern=r"^(bicicleta|moto|patineta)$")
    valor_minimo: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    
class TarifaRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    fecha_actualizacion: datetime
    estado: bool
    fecha_creacion: datetime
    