from pydantic import BaseModel
from typing import Optional, List

from schema.EstoqueSchema import Estoque


# criando classe produto base que vai ser herdada para os metodos produtoCreate e produto
class ProdutoBase(BaseModel):
    nome:               str
    codigo:             str
    categoria:          str
    quantidade_minima:  Optional[int] = 0
    categoria:          str
    preco:              float
    preco_promocional:  float
    descricao:          str
    fornecedor:         str

# classe de criação do produto
class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseModel):
    nome:               Optional[str] = None
    codigo:             Optional[str] = None
    categoria:          Optional[str] = None
    quantidade_minima:  Optional[int] = None
    categoria:          Optional[str] = None
    preco:              Optional[float] = None
    preco_promocional:  Optional[float] = None
    descricao:          Optional[str] = None
    fornecedor:         Optional[str] = None


class Produto(ProdutoBase):
    id: int


# classe getter Produto
class ProdutoEstoque(ProdutoBase):
    id: int
    quantidade: int
    estoque: List[Estoque] = []
