from decimal import Decimal
from datetime import date, time
from pydantic import BaseModel, ConfigDict, Field

class ParseResult(BaseModel):
    banco: str | None = Field(default=None, description="Banco emisor de la notificación")
    tipo_movimiento: str | None = Field(default=None, description="Naturaleza del movimiento reportado")
    concepto: str | None = Field(default=None, description="Concepto o descripción del movimiento")
    monto: Decimal | None = Field(default=None, description="Valor de la operación")
    fecha: date | None = Field(default=None, description="Fecha de la operación")
    hora: time | None = Field(default=None, description="Hora de la operación")
    estado: str | None = Field(default=None, description="Estado de la transacción")
    referencia: str | None = Field(default=None, description="Número de referencia de la operación")

    model_config = ConfigDict(
        frozen=True,
    )
