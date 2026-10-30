from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.pagos import Pago
from app.schemas.pagos import PagoCrear


class PagoRepositorio:

    def listar(self, db: Session) -> list[Pago]:
        consulta: Select(Pago).order_by(Pago.id.desc())
        return list(db.scalars(consulta).all())


    def obtener_por_id(self, db: Session, pago_id: int) -> Pago | None:
        return db.get(Pago, pago_id)

    def obtener_por_movimiento_id(self, db: Session, movimiento_id: int) -> Pago | None:
        consulta: Select(Pago).where(Pago.movimiento_id == movimiento_id)
        return db.scalars(consulta)
    
    def crear(self, db: Session, pago: PagoCrear) -> Pago:
        pago = Pago(**pago.model_dump())
        db.add(pago)
        db.flush()
        return pago
    
pago_repositorio = PagoRepositorio()