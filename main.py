from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from database import Base
from schema import ProdutoSchema
from controller import ProdutoController
from schema import EstoqueSchema
from controller import EstoqueController
from database import SessionLocal, engine

# esse metodo cria nosso banco de dados caso ele não exista
Base.metadata.create_all(bind=engine)

# tags utilizadas para separar nossas rotas
tags_metadata = [
    {
        "name": "Open",
        "description": "Rotas",
    }
]


# instanciando nossa aplicação
app = FastAPI(openapi_tags=tags_metadata)

# metodo de acesso ao banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ROTAS

@app.post("/produto/", response_model=ProdutoSchema.Produto, tags=["Open"])
async def create_produto(produto: ProdutoSchema.ProdutoCreate, db: Session = Depends(get_db)):
    return ProdutoController.create_produto(db, produto=produto)

@app.put("/produto/{produto_id}", response_model=ProdutoSchema.Produto, tags=["Open"])
async def update_produto(produto_id: int, produto: ProdutoSchema.ProdutoUpdate, db: Session = Depends(get_db)):
    return ProdutoController.update_produto(db, produto_id=produto_id, produto=produto)

@app.get("/produtos/", response_model=list[ProdutoSchema.Produto], tags=["Open"])
async def get_produtos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ProdutoController.get_produto(db, skip=skip, limit=limit)

@app.post("/estoque/entrada", response_model=EstoqueSchema.EstoqueCreate, tags=["Open"])
async def add_estoque(estoque: EstoqueSchema.EstoqueCreate, db: Session = Depends(get_db)):
    return EstoqueController.create_estoque(db, estoque=estoque, entrada=True)

@app.post("/estoque/saida", response_model=EstoqueSchema.EstoqueCreate, tags=["Open"])
async def sub_estoque(estoque: EstoqueSchema.EstoqueCreate, db: Session = Depends(get_db)):
    return EstoqueController.create_estoque(db, estoque=estoque, entrada=False)

@app.put("/estoque/{estoque_id}", response_model=EstoqueSchema.Estoque, tags=["Open"])
async def update_estoque(estoque_id: int, estoque: EstoqueSchema.EstoqueUpdate, db: Session = Depends(get_db)):
    return EstoqueController.update_estoque(db, estoque_id=estoque_id, estoque=estoque)

@app.get("/estoques/", response_model=list[EstoqueSchema.Estoque], tags=["Open"])
async def get_estoque(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return EstoqueController.get_estoque(db, skip=skip, limit=limit)


@app.get("/estoque/produtos/", response_model=list[ProdutoSchema.ProdutoEstoque], tags=["Open"])
async def get_produto_estoque(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ProdutoController.get_produto_estoque(db, skip=skip, limit=limit)


@app.get("/estoque/produtos/alertas", response_model=list[ProdutoSchema.ProdutoEstoque], tags=["Open"])
async def get_produto_estoque_alerta(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ProdutoController.get_produto_estoque_alerta(db, skip=skip, limit=limit)


