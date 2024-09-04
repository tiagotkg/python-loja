from pydantic import BaseModel

class EstoqueBase(BaseModel):
    produto_id: str
    quantidade_minima: int
    quantidade: int
    quantidade_maxima: int

class EstoqueCreate(EstoqueBase):
    pass

# classe getter Lixo
class Estoque(EstoqueBase):
    id: int

    class Config:
        from_attributes = True
