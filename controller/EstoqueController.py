from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from model.Estoque import Estoque
from model.Produto import Produto
import schema


# metodo utilizado para listar os estoques cadastrados
def get_estoque(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Estoque).options(joinedload(Estoque.produto)).all()


# metodo utilizado para cadastrar um novo lixo
def create_estoque(db: Session, estoque: schema.EstoqueSchema.EstoqueCreate, entrada: bool):
    db_estoque = Estoque(**estoque.model_dump())
    db_estoque.entrada_saida = entrada

    db_produto = db.query(Produto).filter(Produto.id == db_estoque.produto_id).first()
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    if(entrada):
        db_produto.quantidade = (db_produto.quantidade + db_estoque.quantidade)
    else:
        db_produto.quantidade = (db_produto.quantidade - db_estoque.quantidade)

    if(db_produto.quantidade <= db_produto.quantidade_minima):
        print("Quantidade miníma antigida!")

    db.commit()
    db.add(db_estoque)
    db.commit()
    db.refresh(db_produto)
    db.refresh(db_estoque)

    return db_estoque


def update_estoque(db: Session, estoque_id: int, estoque: schema.EstoqueSchema.EstoqueUpdate):
    db_estoque = db.query(Estoque).filter(Estoque.id == estoque_id).first()
    if db_estoque is None:
        raise HTTPException(status_code=404, detail="Estoque não encontrado")

    for key, value in estoque.model_dump().items():
        if(value):
            setattr(db_estoque, key, value)

    db.commit()
    db.refresh(db_estoque)
    return db_estoque