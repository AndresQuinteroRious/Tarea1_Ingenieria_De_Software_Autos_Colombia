from functools import wraps

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import Pago
from app.schemas.pago import PagoActualizar, PagoCrear


class PagoError(Exception):
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
                raise PagoError(409, "El pago tiene registros relacionados y no se puede eliminar.") from None
            if code in {"23502", "23514"}:
                raise PagoError(422, "Los datos incumplen las restricciones del pago.") from None
            raise PagoError(409, "La operación entra en conflicto con los datos existentes.") from None
        except SQLAlchemyError:
            session.rollback()
            raise PagoError(503, "No se pudo completar la operación con la base de datos.") from None
    return wrapped


def find_pago(session: Session, pago_id: int) -> Pago:
    pago = session.get(Pago, pago_id)
    if pago is None:
        raise PagoError(404, "Pago no encontrado.")
    return pago


@database_operation
def create_pago(session: Session, data: PagoCrear) -> Pago:
    pago = Pago(**data.model_dump())
    session.add(pago)
    session.commit()
    session.refresh(pago)
    return pago


@database_operation
def list_pagos(session: Session, offset: int, limit: int) -> dict:
    total = session.scalar(select(func.count()).select_from(Pago))
    items = list(session.scalars(select(Pago).order_by(Pago.id).offset(offset).limit(limit)))
    return {"items": items, "total": total, "offset": offset, "limit": limit}


@database_operation
def get_pago(session: Session, pago_id: int) -> Pago:
    return find_pago(session, pago_id)


@database_operation
def update_pago(session: Session, pago_id: int, data: PagoActualizar) -> Pago:
    pago = find_pago(session, pago_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(pago, key, value)
    session.commit()
    session.refresh(pago)
    return pago


@database_operation
def delete_pago(session: Session, pago_id: int) -> None:
    pago = find_pago(session, pago_id)
    session.delete(pago)
    session.commit()
