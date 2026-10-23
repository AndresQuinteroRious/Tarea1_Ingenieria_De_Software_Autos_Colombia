from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Response
from sqlalchemy.orm import Session

from app.database import get_session
from app.schemas.novedad import NovedadActualizar, NovedadCrear, NovedadRespuesta, NovedadesPagina
from app.services import novedad as service

router = APIRouter(prefix="/novedades", tags=["Novedades"])
DatabaseSession = Annotated[Session, Depends(get_session)]
NovedadId = Annotated[int, Path(ge=1, le=9223372036854775807)]


@router.post("", response_model=NovedadRespuesta, status_code=201)
def create(data: NovedadCrear, session: DatabaseSession):
    return service.create_novedad(session, data)


@router.get("", response_model=NovedadesPagina)
def list_all(
    session: DatabaseSession,
    offset: Annotated[int, Query(ge=0, le=9223372036854775807)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    return service.list_novedades(session, offset, limit)


@router.get("/{id}", response_model=NovedadRespuesta)
def get_one(id: NovedadId, session: DatabaseSession):
    return service.get_novedad(session, id)


@router.patch("/{id}", response_model=NovedadRespuesta)
def update(id: NovedadId, data: NovedadActualizar, session: DatabaseSession):
    return service.update_novedad(session, id, data)


@router.delete("/{id}", status_code=204)
def delete(id: NovedadId, session: DatabaseSession) -> Response:
    service.delete_novedad(session, id)
    return Response(status_code=204)
