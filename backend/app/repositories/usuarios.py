from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.usuarios import Usuario
from app.schemas.usuarios import UsuarioCrear, UsuarioActualizar

class UsuarioRepositorio:

    def listar(self, db: Session) -> list[Usuario]:
        consulta = select(Usuario).order_by(Usuario.id)
        return list(db.scalars(consulta).all())
    
    def obtener_por_id(self, db: Session, usuario_id: int) -> Usuario | None:
        return db.get(Usuario, usuario_id)
    
    def obtener_por_correo(self, db: Session, correo: str) -> Usuario | None:
        consulta = select(Usuario).where(Usuario.correo == correo)
        return db.scalars(consulta).first()
    
    def crear(self, db: Session, datos: UsuarioCrear) -> Usuario:
        usuario = Usuario(**datos.model_dump())
        db.add(usuario)
        db.flush()
        return usuario

    def actualizar(self, db: Session, usuario: Usuario, datos: UsuarioActualizar) -> Usuario:
        cambios = datos.model_dump(exclude_unset=True)
        
        for campo, valor in cambios.items():
            setattr(usuario, campo, valor)
        
        db.flush()
        return usuario

    def desactivar(self, db: Session, usuario: Usuario) -> Usuario:
        usuario.estado = False
        db.flush()
        return usuario

usuario_repositorio = UsuarioRepositorio()