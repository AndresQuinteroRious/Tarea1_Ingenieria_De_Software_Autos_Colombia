from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

from app.models import required_text


Texto = Annotated[str, BeforeValidator(lambda value: required_text(value, "El campo"))]
ValorPago = Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]


class PagoCrear(BaseModel):
    model_config = ConfigDict(extra="forbid")

    valor: ValorPago
    periodo: Texto


class PagoActualizar(BaseModel):
    model_config = ConfigDict(extra="forbid")

    valor: ValorPago | None = None
    periodo: Texto | None = None

    @classmethod
    def reject_null(cls, value):
        if value is None:
            raise ValueError("Los campos enviados no pueden ser nulos.")
        return value


class PagoRespuesta(PagoCrear):
    model_config = ConfigDict(from_attributes=True, extra="forbid")
    id: int
    fecha: datetime


class PagosPagina(BaseModel):
    items: list[PagoRespuesta]
    total: int
    offset: int
    limit: int
