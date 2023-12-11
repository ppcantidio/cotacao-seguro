from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class CotarSeguroPayload(BaseModel):
    nome: str
    cpf: str
    idade: int
    email: str
    genero_biologico: Literal["M", "F"]
    vl_importancia_segurada: int
    dt_inicio_vigencia: datetime
    dt_fim_vigencia: datetime


class CotarSeguroResponse(BaseModel):
    vl_premio_bruto: int
    vl_premio_liquido: int
    vl_iof: int
    vl_corretagem: int
