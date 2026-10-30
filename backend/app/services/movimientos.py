from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from app.repositories.movimientos import movimiento_repositorio
from app.repositories.vehiculos import vehiculo_repositorio
from app.repositories.usuarios import usuario_repositorio
from app.repositories.tarifas import tarifa_repositorio
from app.schemas.movimientos import MovimientoCrear
from app.models.movimientos import Movimiento

class MovimientoService:
    
    def listar_movimientos(self, db: Session):
        return movimiento_repositorio.listar(db)
    
    def listar_activos(self, db: Session):
        return movimiento_repositorio.listar_activos(db)
    
    def obtener_movimiento(self, db: Session, movimiento_id: int):
        movimiento = movimiento_repositorio.obtener_por_id(db, movimiento_id)
        
        if movimiento is None:
            raise ValueError(f"El movimiento con ID {movimiento_id} no existe")
        return movimiento
    
    def registrar_entrada(self, db: Session, datos: MovimientoCrear):
        vehiculo = vehiculo_repositorio.obtener_por_id(db, datos.vehiculo_id)
        if vehiculo is None or not vehiculo.estado:
            raise ValueError(f"El vehículo con ID {datos.vehiculo_id} no existe o no está disponible")
        
        movimiento_activo = movimiento_repositorio.obtener_por_vehiculo(db, datos.vehiculo_id)
        if movimiento_activo is not None:
            raise ValueError(f"El vehículo con ID {datos.vehiculo_id} ya tiene un movimiento activo")
        
        if datos.usuario_ingreso_id is not None:
            usuario = usuario_repositorio.obtener_por_id(db, datos.usuario_ingreso_id)
            if usuario is None or not usuario.estado:
                raise ValueError(f"El usuario con ID {datos.usuario_ingreso_id} no existe")
            
        try:
            movimiento = movimiento_repositorio.crear(db, datos)
            db.commit()
            db.refresh(movimiento)
            return movimiento
        except Exception:
            db.rollback()
            raise
        
    def finalizar_salida(self, db: Session, movimiento_id: int, usuario_salida_id: int | None = None):
        movimiento = self.obtener_movimiento(db, movimiento_id)
        
        if movimiento.estado != "ACTIVO":
            raise ValueError(f"El movimiento con ID {movimiento_id} no está activo y no puede ser finalizado")
        
        if usuario_salida_id is not None:
            usuario = usuario_repositorio.obtener_por_id(db, usuario_salida_id)
            if usuario is None or not usuario.estado:
                raise ValueError(f"El usuario con ID {usuario_salida_id} no existe")
            
        vehiculo = vehiculo_repositorio.obtener_por_id(db, movimiento.vehiculo_id)
        if vehiculo is None:
            raise ValueError(f"El vehiculo con ID {movimiento.vehiculo_id} no se encontro el movimiento del vehiculo")
        
        tarifa = tarifa_repositorio.obtener_por_tipo(db, vehiculo.tipo_vehiculo)
        if tarifa is None or not tarifa.estado:
            raise ValueError(f"La tarifa para el tipo de vehiculo {vehiculo.tipo_vehiculo} no existe")
        
        try:
            ahora = datetime.now()
            duracion = ahora - movimiento.fecha_ingreso
            segundos = max(0, int(duracion.total_seconds()))
            minutos = max(1, (segundos + 59) // 60)
            valor = (Decimal(minutos) * Decimal(str(tarifa.valor_minuto))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            
            movimiento_fecha_salida = ahora
            movimiento_valor_total = valor
            movimiento_estado = "FINALIZADO"
            movimiento_minutos = minutos
            movimiento_usuario_salida_id = usuario_salida_id
            
            db.flush()
            db.commit()
            db.refresh(movimiento)
            
            return movimiento
        except Exception:
            db.rollback()
            raise

movimiento_servicio = MovimientoService()