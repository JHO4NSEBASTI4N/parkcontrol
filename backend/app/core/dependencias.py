from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.seguridad import decodificar_token
from app.database.connection import obtener_sesion
from app.models.usuarios import Usuario


esquema_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def obtener_usuario_actual(
    token: Annotated[str, Depends(esquema_oauth2)],
    db: Annotated[Session, Depends(obtener_sesion)],
) -> Usuario:
    error_credenciales = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        contenido = decodificar_token(token)
        identificador = contenido.get("sub")

        if not identificador:
            raise error_credenciales

        usuario_id = int(identificador)
        
    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise error_credenciales

    usuario = db.get(Usuario, usuario_id)

    if usuario is None or not usuario.estado:
        raise error_credenciales

    return usuario


def exigir_administrador(
    usuario: Annotated[Usuario, Depends(obtener_usuario_actual)],
) -> Usuario:
    if usuario.rol != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador.",
        )

    return usuario