from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from app.repositories.usuarios import usuario_repositorio
from app.schemas.usuarios import UsuarioCrear, UsuarioActualizar


gestor_contrasenas = PasswordHash.recommended()


class UsuarioServicio:

    def listar_usuarios(self, db: Session):
        return usuario_repositorio.listar(db)

    def obtener_usuario(self, db: Session, usuario_id: int):
        usuario = usuario_repositorio.obtener_por_id(db, usuario_id)

        if usuario is None:
            raise ValueError("El usuario no existe.")

        return usuario

    def obtener_usuario_por_correo(
        self,
        db: Session,
        correo: str,
    ):
        return usuario_repositorio.obtener_por_correo(db, correo)

    def verificar_contrasena(
        self,
        contrasena: str,
        hash_guardado: str,
    ) -> bool:
        return gestor_contrasenas.verify(
            contrasena,
            hash_guardado,
        )

    def crear_usuario(self, db: Session, datos: UsuarioCrear):
        correo = str(datos.correo)

        existente = usuario_repositorio.obtener_por_correo(
            db,
            correo,
        )

        if existente is not None:
            raise ValueError(
                "Ya existe un usuario con ese correo electrónico."
            )

        try:
            datos_usuario = datos.model_dump(exclude={"password"})
            datos_usuario["correo"] = correo
            datos_usuario["password_hash"] = gestor_contrasenas.hash(
                datos.password
            )

            usuario = usuario_repositorio.crear(
                db,
                datos_usuario,
            )

            db.commit()
            db.refresh(usuario)
            return usuario

        except Exception:
            db.rollback()
            raise

    def actualizar_usuario(
        self,
        db: Session,
        usuario_id: int,
        datos: UsuarioActualizar,
    ):
        usuario = self.obtener_usuario(db, usuario_id)

        cambios = datos.model_dump(exclude_unset=True)

        # Impedir valores nulos en campos obligatorios.
        for campo in ("nombre", "correo", "rol", "estado"):
            if campo in cambios and cambios[campo] is None:
                raise ValueError(
                    f"El campo '{campo}' no puede ser nulo."
                )

        nuevo_correo = cambios.get("correo")

        if nuevo_correo is not None:
            nuevo_correo = str(nuevo_correo)

            if nuevo_correo != usuario.correo:
                existente = usuario_repositorio.obtener_por_correo(
                    db,
                    nuevo_correo,
                )

                if existente is not None:
                    raise ValueError(
                        "Ya existe otro usuario con ese correo electrónico."
                    )

            cambios["correo"] = nuevo_correo

        nueva_contrasena = cambios.pop("password", None)

        if nueva_contrasena is not None:
            cambios["password_hash"] = gestor_contrasenas.hash(
                nueva_contrasena
            )

        try:
            usuario = usuario_repositorio.actualizar(
                db,
                usuario,
                cambios,
            )

            db.commit()
            db.refresh(usuario)
            return usuario

        except Exception:
            db.rollback()
            raise

    def desactivar_usuario(self, db: Session, usuario_id: int):
        usuario = self.obtener_usuario(db, usuario_id)

        try:
            usuario = usuario_repositorio.desactivar(db, usuario)
            db.commit()
            db.refresh(usuario)
            return usuario

        except Exception:
            db.rollback()
            raise


usuario_servicio = UsuarioServicio()