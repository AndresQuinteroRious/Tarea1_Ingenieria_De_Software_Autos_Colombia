from functools import wraps

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import Novedad
from app.schemas.novedad import NovedadActualizar, NovedadCrear


class NovedadError(Exception):
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
            if code == "23503":
                raise NovedadError(409, "La novedad tiene registros relacionados y no se puede eliminar.") from None
            if code in {"23502", "23514"}:
                raise NovedadError(422, "Los datos incumplen las restricciones de la novedad.") from None
            raise NovedadError(409, "La operación entra en conflicto con los datos existentes.") from None
        except SQLAlchemyError:
            session.rollback()
            raise NovedadError(503, "No se pudo completar la operación con la base de datos.") from None
    return wrapped


def find_novedad(session: Session, novedad_id: int) -> Novedad:
    novedad = session.get(Novedad, novedad_id)
    if novedad is None:
        raise NovedadError(404, "Novedad no encontrada.")
    return novedad


@database_operation
def create_novedad(session: Session, data: NovedadCrear) -> Novedad:
    novedad = Novedad(**data.model_dump())
    session.add(novedad)
    session.commit()
    session.refresh(novedad)
    return novedad


@database_operation
def list_novedades(session: Session, offset: int, limit: int) -> dict:
    total = session.scalar(select(func.count()).select_from(Novedad))
    items = list(session.scalars(select(Novedad).order_by(Novedad.id).offset(offset).limit(limit)))
    return {"items": items, "total": total, "offset": offset, "limit": limit}


@database_operation
def get_novedad(session: Session, novedad_id: int) -> Novedad:
    return find_novedad(session, novedad_id)


@database_operation
def update_novedad(session: Session, novedad_id: int, data: NovedadActualizar) -> Novedad:
    novedad = find_novedad(session, novedad_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(novedad, key, value)
    session.commit()
    session.refresh(novedad)
    return novedad


@database_operation
def delete_novedad(session: Session, novedad_id: int) -> None:
    novedad = find_novedad(session, novedad_id)
    session.delete(novedad)
    session.commit()
