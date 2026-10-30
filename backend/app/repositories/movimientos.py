from sqlalchemy import Select
from sqlalchemy.orm import Session

from app.models.movimientos import Movimiento
from app.schemas.movimientos import MovimientoCrear, MovimientoFinalizar

class MovimientoRepositorio:
    
    def listar(self, db: Session) -> list[Movimiento]:
        consulta: Select(Movimiento).order_by(Movimiento.id.desc())
        return list(db.scalars(consulta).all())
    
    def obtener_por_id(self, db: Session, movimiento_id: int) -> Movimiento | None:
        return db.get(Movimiento, movimiento_id)
    
    def obtener_por_vehiculo_id(self, db: Session, vehiculo_id: int) -> Movimiento | None:
        consulta: Select(Movimiento).where(Movimiento.vehiculo_id == vehiculo_id, Movimiento.estado == "ACTIVO")
        return db.scalar(consulta)
    
    def listar_activos(self, db: Session) -> list[Movimiento]:
        consulta: Select(Movimiento).where(Movimiento.estado == "ACTIVO").order_by(Movimiento.fecha_ingreso.desc())
        return list(db.scalars(consulta).all())
        
    def crear(self, db: Session, datos: MovimientoCrear) -> Movimiento:
        movimiento = Movimiento(**datos.model_dump())
        db.add(movimiento)
        db.flush()
        return movimiento
    
movimiento_repositorio = MovimientoRepositorio()