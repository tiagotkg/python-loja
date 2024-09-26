from pydantic import BaseModel
from typing import Optional, List

from schema.EstoqueSchema import Estoque
from schema.ProdutoSchema import Produto


# criando classe produto base que vai ser herdada para os metodos produtoCreate e produto
class VendaProdutoBase(BaseModel):
    venda_id    : int
    produto_id  : int
    quantidade  : int
    valor       : float

# classe de criação do produto
class VendaProdutoCreate(BaseModel):
    produto_id  : int
    quantidade  : int

class VendaProdutoUpdate(BaseModel):
    pass


class VendaProduto(VendaProdutoBase):
    id: int
    produto: Produto
    class Config:
        from_attributes = True
