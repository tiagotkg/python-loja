from pydantic import BaseModel

class EstoqueBase(BaseModel):
    produto_id:     int
    quantidade:     int
    entrada_saida:  int


class EstoqueCreate(BaseModel):
    produto_id: int
    quantidade: int


class EstoqueUpdate(EstoqueBase):
    pass


# classe getter Estoque
class Estoque(EstoqueBase):
    id: int

    class Config:
        from_attributes = True

