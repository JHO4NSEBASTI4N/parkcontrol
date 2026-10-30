from sqlalchemy.orm import Session

from app.repositories.vehiculos import vehiculo_repositorio
from app.repositories.clientes import cliente_repositorio
from app.schemas.vehiculos import VehiculoCrear, VehiculoActualizar


class VehiculoServicio:

    def listar_vehiculos(self, db: Session):
        return vehiculo_repositorio.listar(db)

    def obtener_vehiculo(self, db: Session, vehiculo_id: int):
        vehiculo = vehiculo_repositorio.obtener_por_id(db, vehiculo_id)

        if vehiculo is None:
            raise ValueError("El vehículo no existe.")

        return vehiculo

    def validar_cliente(self, db: Session, cliente_id: int):
        cliente = cliente_repositorio.obtener_por_id(db, cliente_id)

        if cliente is None or not cliente.estado:
            raise ValueError("El cliente no existe o está inactivo.")

        return cliente

    def validar_codigo(
        self, db: Session, codigo: str, excluir_id: int | None = None
    ):
        existente = vehiculo_repositorio.obtener_por_codigo(db, codigo)

        if existente is not None and existente.id != excluir_id:
            raise ValueError("Ya existe un vehículo con ese código.")

    def validar_placa(
        self, db: Session, placa: str | None,
        excluir_id: int | None = None
    ):
        if not placa:
            return

        existente = vehiculo_repositorio.obtener_por_placa(db, placa)

        if existente is not None and existente.id != excluir_id:
            raise ValueError("Ya existe un vehículo con esa placa.")

    def crear_vehiculo(self, db: Session, datos: VehiculoCrear):
        self.validar_cliente(db, datos.cliente_id)
        self.validar_codigo(db, datos.codigo)
        self.validar_placa(db, datos.placa)

        try:
            vehiculo = vehiculo_repositorio.crear(db, datos)
            db.commit()
            db.refresh(vehiculo)
            return vehiculo
        except Exception:
            db.rollback()
            raise

    def actualizar_vehiculo(
        self, db: Session, vehiculo_id: int, datos: VehiculoActualizar
    ):
        vehiculo = self.obtener_vehiculo(db, vehiculo_id)
        cambios = datos.model_dump(exclude_unset=True)

        if "cliente_id" in cambios and cambios["cliente_id"] is not None:
            self.validar_cliente(db, cambios["cliente_id"])

        if cambios.get("codigo") is not None:
            self.validar_codigo(
                db, cambios["codigo"], excluir_id=vehiculo_id
            )

        if "placa" in cambios:
            self.validar_placa(
                db, cambios["placa"], excluir_id=vehiculo_id
            )

        try:
            vehiculo = vehiculo_repositorio.actualizar(
                db, vehiculo, datos
            )
            db.commit()
            db.refresh(vehiculo)
            return vehiculo
        except Exception:
            db.rollback()
            raise

    def desactivar_vehiculo(self, db: Session, vehiculo_id: int):
        vehiculo = self.obtener_vehiculo(db, vehiculo_id)

        try:
            vehiculo = vehiculo_repositorio.desactivar(db, vehiculo)
            db.commit()
            db.refresh(vehiculo)
            return vehiculo
        except Exception:
            db.rollback()
            raise


vehiculo_servicio = VehiculoServicio()