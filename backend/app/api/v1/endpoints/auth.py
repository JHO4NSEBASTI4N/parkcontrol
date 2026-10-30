from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.seguridad import crear_token_acceso
from app.database.connection import obtener_sesion
from app.services.usuarios import usuario_servicio


router = APIRouter(
    prefix="/api/auth",
    tags=["Autenticación"],
)


@router.post("/login")
def iniciar_sesion(
    formulario: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(obtener_sesion)],
):
    # OAuth2PasswordRequestForm utiliza el campo "username".
    # En ParkControl lo empleamos para recibir el correo electrónico.
    correo = formulario.username.strip()

    usuario = usuario_servicio.obtener_usuario_por_correo(
        db,
        correo,
    )

    # Rechazar credenciales incorrectas y cuentas desactivadas.
    if (
        usuario is None
        or not usuario.estado
        or not usuario_servicio.verificar_contrasena(
            formulario.password,
            usuario.password_hash,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # El identificador se almacena como texto en el claim "sub".
    token = crear_token_acceso(
        {"sub": str(usuario.id)}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }