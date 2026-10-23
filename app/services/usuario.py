from functools import wraps

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import Usuario
from app.schemas.usuario import UsuarioActualizar, UsuarioCrear


class UsuarioError(Exception):
    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail


def database_operation(operation):
    """Centraliza rollback y mensajes públicos sin detalles del driver."""
    @wraps(operation)
    def wrapped(session: Session, *args, **kwargs):
        try:
            return operation(session, *args, **kwargs)
        except IntegrityError as error:
            session.rollback()
            code = getattr(error.orig, "sqlstate", None)
            constraint = getattr(getattr(error.orig, "diag", None), "constraint_name", None)
            if code == "23505" and constraint == "uq_usuario_documento":
                raise UsuarioError(409, "Ya existe un usuario con ese documento.") from None
            if code == "23503":
                raise UsuarioError(409, "El usuario tiene registros relacionados y no se puede eliminar.") from None
            if code in {"23502", "23514"}:
                raise UsuarioError(422, "Los datos incumplen las restricciones del usuario.") from None
            raise UsuarioError(409, "La operación entra en conflicto con los datos existentes.") from None
        except SQLAlchemyError:
            session.rollback()
            raise UsuarioError(503, "No se pudo completar la operación con la base de datos.") from None
    return wrapped


def find_user(session: Session, user_id: int) -> Usuario:
    user = session.get(Usuario, user_id)
    if user is None:
        raise UsuarioError(404, "Usuario no encontrado.")
    return user


@database_operation
def create_user(session: Session, data: UsuarioCrear) -> Usuario:
    user = Usuario(**data.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@database_operation
def list_users(session: Session, offset: int, limit: int) -> dict:
    total = session.scalar(select(func.count()).select_from(Usuario))
    items = list(session.scalars(select(Usuario).order_by(Usuario.id).offset(offset).limit(limit)))
    return {"items": items, "total": total, "offset": offset, "limit": limit}


@database_operation
def get_user(session: Session, user_id: int) -> Usuario:
    return find_user(session, user_id)


@database_operation
def update_user(session: Session, user_id: int, data: UsuarioActualizar) -> Usuario:
    user = find_user(session, user_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    session.commit()
    session.refresh(user)
    return user


@database_operation
def delete_user(session: Session, user_id: int) -> None:
    user = find_user(session, user_id)
    session.delete(user)
    session.commit()
