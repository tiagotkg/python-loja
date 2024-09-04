from sqlalchemy.orm import Session

from model.Produto import Produto
import schema


# metodo utilizado para listar os lixos cadastrados
def get_produto(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Produto).offset(skip).limit(limit).all()


# metodo utilizado para cadastrar um novo lixo
def create_produto(db: Session, produto: schema.ProdutoSchema):
    db_produto = Produto(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto