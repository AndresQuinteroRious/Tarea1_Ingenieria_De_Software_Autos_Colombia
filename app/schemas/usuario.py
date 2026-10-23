from datetime import date
from typing import Annotated

from pydantic import AfterValidator, BaseModel, BeforeValidator, ConfigDict, Field

from app.models import required_text


Texto = Annotated[str, BeforeValidator(lambda value: required_text(value, "El campo"))]
Documento = Annotated[Texto, AfterValidator(str.upper)]
FechaVencimiento = Annotated[date, Field(ge=date(1900, 1, 1))]


class UsuarioCrear(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nombre: Texto
    documento: Documento
    telefono: Texto
    fecha_vencimiento: FechaVencimiento


class UsuarioActualizar(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nombre: Texto | None = None
    documento: Documento | None = None
    telefono: Texto | None = None
    fecha_vencimiento: FechaVencimiento | None = None

    @classmethod
    def reject_null(cls, value):
        if value is None:
            raise ValueError("Los campos enviados no pueden ser nulos.")
        return value


class UsuarioRespuesta(UsuarioCrear):
    model_config = ConfigDict(from_attributes=True, extra="forbid")
    id: int


class UsuariosPagina(BaseModel):
    items: list[UsuarioRespuesta]
    total: int
    offset: int
    limit: int
