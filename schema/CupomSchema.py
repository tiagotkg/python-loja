from datetime import datetime

from pydantic import BaseModel
from typing import Optional, List

from sqlalchemy import DateTime

from schema.EstoqueSchema import Estoque


# criando classe produto base que vai ser herdada para os metodos produtoCreate e produto
class CupomBase(BaseModel):
    codigo      : str
    porcentagem : bool
    valor       : float
    ativo       : bool

# classe de criação do Cupom
class CupomCreate(CupomBase):
    pass

class CupomUpdate(BaseModel):
    ativo: bool


class CupomDelete(BaseModel):
    deleted_at: datetime

class Cupom(CupomBase):
    id: int

