from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Response
from sqlalchemy.orm import Session

from app.database import get_session
from app.schemas.pago import PagoActualizar, PagoCrear, PagoRespuesta, PagosPagina
from app.services import pago as service

router = APIRouter(prefix="/pagos", tags=["Pagos"])
DatabaseSession = Annotated[Session, Depends(get_session)]
PagoId = Annotated[int, Path(ge=1, le=9223372036854775807)]


@router.post("", response_model=PagoRespuesta, status_code=201)
def create(data: PagoCrear, session: DatabaseSession):
    return service.create_pago(session, data)


@router.get("", response_model=PagosPagina)
def list_all(
    session: DatabaseSession,
    offset: Annotated[int, Query(ge=0, le=9223372036854775807)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    return service.list_pagos(session, offset, limit)


@router.get("/{id}", response_model=PagoRespuesta)
def get_one(id: PagoId, session: DatabaseSession):
    return service.get_pago(session, id)


@router.patch("/{id}", response_model=PagoRespuesta)
def update(id: PagoId, data: PagoActualizar, session: DatabaseSession):
    return service.update_pago(session, id, data)


@router.delete("/{id}", status_code=204)
def delete(id: PagoId, session: DatabaseSession) -> Response:
    service.delete_pago(session, id)
    return Response(status_code=204)
