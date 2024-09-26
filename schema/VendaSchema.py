from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from schema.VendaProdutoSchema import VendaProduto, VendaProdutoBase, VendaProdutoCreate


# criando classe produto base que vai ser herdada para os metodos produtoCreate e produto
class VendaBase(BaseModel):
    data        : datetime
    sub_total   : float
    cupom_id    : Optional[int] = None
    desconto    : Optional[float] = None
    total       : float

# classe de criação do produto
class VendaCreate(BaseModel):
    cupom    : Optional[str] = None
    produtos    : List[VendaProdutoCreate]

class VendaUpdate(VendaBase):
    pass

class Venda(VendaBase):
    id: int


# classe getter Venda
class VendaProdutos(VendaBase):
    id: int
    venda_produto: List[VendaProduto]

    class Config:
        from_attributes = True
