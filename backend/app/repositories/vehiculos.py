from sqlalchemy.orm import Session
from sqlalchemy import Select

from app.models.vehiculos import Vehiculo
from app.schemas.vehiculos import VehiculoCrear, VehiculoActualizar

class VehiculoRepositorio:

    def listar(self, db: Session) -> list[Vehiculo]:
        consulta: Select(Vehiculo).order_by(Vehiculo.id)
        return list(db.scalars(consulta).all())
    
    def obtener_por_id(self, db: Session, vehiculo_id: int) -> Vehiculo | None:
        return db.get(Vehiculo, vehiculo_id)
    
    def obtener_por_codigo(self, db: Session, codigo: str) -> Vehiculo | None:
        consulta: Select(Vehiculo).where(Vehiculo.codigo == codigo)
        return db.scalars(consulta).first()
    
    def obtener_por_placa(self, db: Session, placa: str) -> Vehiculo | None:
        consulta: Select(Vehiculo).where(Vehiculo.placa == placa)
        return db.scalars(consulta)

    def crear(self, db: Session, datos: VehiculoCrear) -> Vehiculo:
        vehiculo = Vehiculo(**datos.model_dump())
        db.add(vehiculo)
        db.flush()
        return vehiculo
    
    def actualizar(self, db: Session, vehiculo: Vehiculo, datos: VehiculoActualizar) -> Vehiculo:
        cambios = datos.model_dump(exclude_unset=True)
        
        for campo, valor in cambios.items():
            setattr(vehiculo, campo, valor)
        
        db.flush()
        return vehiculo
    
    def desactivar(self, db: Session, vehiculo: Vehiculo) -> Vehiculo:
        vehiculo.estado = False
        db.flush()
        return vehiculo
    
vehiculo_repositorio = VehiculoRepositorio()