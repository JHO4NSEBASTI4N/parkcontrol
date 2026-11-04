from datetime import date, datetime, time, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.connection import obtener_sesion
from app.models.clientes import Cliente
from app.models.movimientos import Movimiento
from app.models.pagos import Pago
from app.schemas.dashboard import DashboardResumen
from app.core.dependencias import obtener_usuario_actual

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
)

@router.get("/resumen", response_model=DashboardResumen)
def obtener_resumen_dashboard(
    db: Session = Depends(obtener_sesion),
    usuario_actual = Depends(obtener_usuario_actual),
):
    hoy = date.today()
    inicio_dia = datetime.combine(hoy, time.min)
    inicio_manana = inicio_dia + timedelta(days=1)

    vehiculos_estacionados = db.scalar(
        select(func.count(Movimiento.id)).where(
            Movimiento.estado == "ACTIVO"
        )
    ) or 0

    ingresos_hoy = db.scalar(
        select(func.coalesce(func.sum(Pago.valor), 0)).where(
            Pago.estado == "PAGADO",
            Pago.fecha_pago >= inicio_dia,
            Pago.fecha_pago < inicio_manana,
        )
    ) or 0

    clientes_registrados = db.scalar(
        select(func.count(Cliente.id)).where(
            Cliente.estado.is_(True)
        )
    ) or 0

    movimientos_hoy = db.scalar(
        select(func.count(Movimiento.id)).where(
            Movimiento.fecha_ingreso >= inicio_dia,
            Movimiento.fecha_ingreso < inicio_manana,
        )
    ) or 0

    return DashboardResumen(
        vehiculos_estacionados=vehiculos_estacionados,
        ingresos_hoy=ingresos_hoy,
        clientes_registrados=clientes_registrados,
        movimientos_hoy=movimientos_hoy,
    )