from pydantic import BaseModel, ConfigDict, Field


class VehiculoBase(BaseModel):
    codigo: str = Field(min_length=1, max_length=20)
    placa: str | None = Field(default=None, min_length=1, max_length=20)
    tipo: str = Field(pattern=r"^(bicicleta|moto|patineta)$")
    marca: str | None = Field(default=None, min_length=1, max_length=50)
    modelo: str | None = Field(default=None, min_length=1, max_length=50)
    color: str | None = Field(default=None, min_length=1, max_length=30)
    
    
class VehiculoCrear(VehiculoBase):
    cliente_id: int = Field(gt=0)
    
    
class VehiculoActualizar(BaseModel):
    codigo: str | None = Field(default=None, min_length=1, max_length=20)
    placa: str | None = Field(default=None, min_length=1, max_length=10)
    tipo: str | None = Field(default=None, pattern=r"^(bicicleta|moto|patineta)$")
    marca: str | None = Field(default=None, min_length=1, max_length=50)
    modelo: str | None = Field(default=None, min_length=1, max_length=50)
    color: str | None = Field(default=None, min_length=1, max_length=30)
    cliente_id: int | None = Field(default=None, gt=0)
    
    
class VehiculoRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    placa: str | None
    tipo: str
    marca: str | None
    modelo: str | None
    color: str | None
    cliente_id: int
    estado: bool