from decimal import Decimal

from sqlalchemy.orm import Session
from app.schemas.pagos import PagoCrear
from app.repositories.pagos import pago_repositorio
from app.repositories.movimientos import movimiento_repositorio

class PagoServicio:
    
    def listar_pagos(self, db: Session):
        return pago_repositorio.listar(db)
    
    def obtener_pago(self, db: Session, pago_id: int):
        pago = pago_repositorio.obtener_por_id(db, pago_id)
        
        if pago is None:
            raise ValueError(f"El pago con ID {pago_id} no existe")
        return pago
    
    def registrar_pago(self, db: Session, datos: PagoCrear):
        movimiento = movimiento_repositorio.obtener_por_id(db, datos.movimiento_id)
        if movimiento is None:
            raise ValueError(f"El movimiento con ID {datos.movimiento_id} no existe")
        
        if movimiento.estado != "FINALIZADO":
            raise ValueError(f"El movimiento con ID {datos.movimiento_id} no está finalizado")
        
        if movimiento.valor_total is None:
            raise ValueError(f"El movimiento con ID {datos.movimiento_id} no tiene un valor total calculado")
        
        valor_recibido = Decimal(str(datos.valor))
        valor_calculado = Decimal(str(movimiento.valor_total))
        
        if valor_recibido != valor_calculado:
            raise ValueError(f"El pago debe ser {valor_calculado} COP.")
        
        pago_existente = pago_repositorio.obtener_por_movimiento(db, datos.movimiento_id)
        if pago_existente is not None:
            raise ValueError(f"Ya existe un pago para el movimiento con ID {datos.movimiento_id}")
        
        try:
            pago = pago_repositorio.crear(db, datos)
            db.commit()
            db.refresh(pago)
            return pago
        except Exception:
            db.rollback()
            raise
        
pago_servicio = PagoServicio()