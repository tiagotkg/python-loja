from pydantic import BaseModel

# criando classe produto base que vai ser herdada para os metodos produtoCreate e produto
class ProdutoBase(BaseModel):
    nome: str
    codigo: int
    categoria: str
    preco: float
    preco_promocinal: float
    descricao: str

# classe de criação do produto
class ProdutoCreate(ProdutoBase):
    pass

# classe getter Produto
class Produto(ProdutoBase):
    id: int

    class Config:
        from_attributes = True