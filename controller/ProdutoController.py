from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException

from model.Produto import Produto
from model.Estoque import Estoque
import schema


# metodo utilizado para listar os lixos cadastrados
def get_produto(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Produto).offset(skip).limit(limit).all()


def get_produto_estoque(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Produto).options(joinedload(Produto.estoque)).offset(skip).limit(limit).all()

def get_produto_estoque_alerta(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Produto).options(joinedload(Produto.estoque)).filter(Produto.quantidade <= Produto.quantidade_minima).all()

# metodo utilizado para cadastrar um novo lixo
def create_produto(db: Session, produto: schema.ProdutoSchema.ProdutoCreate):
    db_produto = Produto(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto


def update_produto(db: Session, produto_id: int, produto: schema.ProdutoSchema.ProdutoUpdate):
    db_produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    for key, value in produto.model_dump().items():
        if(value):
            setattr(db_produto, key, value)

    db.commit()
    db.refresh(db_produto)
    return db_produto