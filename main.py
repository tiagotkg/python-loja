from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from sqlalchemy.orm import Session
from database import Base
from schema import ProdutoSchema, CupomSchema, VendaSchema, EstoqueSchema
from controller import ProdutoController, CupomController, VendaController
from controller import EstoqueController
from database import SessionLocal, engine
from fastapi.templating import Jinja2Templates
import pandas as pd
import io


# esse metodo cria nosso banco de dados caso ele não exista
Base.metadata.create_all(bind=engine)

# tags utilizadas para separar nossas rotas
tags_metadata = [
    {"name": "Produtos", "description": "Rotas dos produtos", },
    {"name": "Estoques", "description": "Rotas dos estoques", },
    {"name": "Cupons", "description": "Rotas dos cupons", },
    {"name": "Vendas", "description": "Rotas das vendas", },
    {"name": "Relatórios", "description": "Rotas dos relatórios", }
]


# instanciando nossa aplicação
app = FastAPI(openapi_tags=tags_metadata)
templates = Jinja2Templates(directory="templates")

# metodo de acesso ao banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ROTAS

@app.post("/produto/", response_model=ProdutoSchema.Produto, tags=["Produtos"])
async def create_produto(produto: ProdutoSchema.ProdutoCreate, db: Session = Depends(get_db)):
    return ProdutoController.create_produto(db, produto=produto)

@app.put("/produto/{produto_id}", response_model=ProdutoSchema.Produto, tags=["Produtos"])
async def update_produto(produto_id: int, produto: ProdutoSchema.ProdutoUpdate, db: Session = Depends(get_db)):
    return ProdutoController.update_produto(db, produto_id=produto_id, produto=produto)

@app.get("/produtos/", response_model=list[ProdutoSchema.Produto], tags=["Produtos"])
async def get_produtos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ProdutoController.get_produto(db, skip=skip, limit=limit)

@app.post("/estoque/entrada", response_model=EstoqueSchema.EstoqueCreate, tags=["Estoques"])
async def add_estoque(estoque: EstoqueSchema.EstoqueCreate, db: Session = Depends(get_db)):
    return EstoqueController.create_estoque(db, estoque=estoque, entrada=True)

@app.post("/estoque/saida", response_model=EstoqueSchema.EstoqueCreate, tags=["Estoques"])
async def sub_estoque(estoque: EstoqueSchema.EstoqueCreate, db: Session = Depends(get_db)):
    return EstoqueController.create_estoque(db, estoque=estoque, entrada=False)

@app.put("/estoque/{estoque_id}", response_model=EstoqueSchema.Estoque, tags=["Estoques"])
async def update_estoque(estoque_id: int, estoque: EstoqueSchema.EstoqueUpdate, db: Session = Depends(get_db)):
    return EstoqueController.update_estoque(db, estoque_id=estoque_id, estoque=estoque)

@app.get("/estoques/", response_model=list[EstoqueSchema.Estoque], tags=["Estoques"])
async def get_estoque(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return EstoqueController.get_estoque(db, skip=skip, limit=limit)

@app.get("/estoque/produtos/", response_model=list[ProdutoSchema.ProdutoEstoque], tags=["Estoques"])
async def get_produto_estoque(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ProdutoController.get_produto_estoque(db, skip=skip, limit=limit)

@app.get("/estoque/produtos/alertas", response_model=list[ProdutoSchema.ProdutoEstoque], tags=["Estoques"])
async def get_produto_estoque_alerta(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ProdutoController.get_produto_estoque_alerta(db, skip=skip, limit=limit)


@app.post("/cupom/", response_model=CupomSchema.Cupom, tags=["Cupons"])
async def create_cupom(cupom: CupomSchema.CupomCreate, db: Session = Depends(get_db)):
    return CupomController.create_cupom(db, cupom=cupom)

@app.put("/cupom/{cupom_id}", response_model=CupomSchema.Cupom, tags=["Cupons"])
async def activate_deactivate_cupom(cupom_id: int, cupom: CupomSchema.CupomUpdate, db: Session = Depends(get_db)):
    return CupomController.update_cupom(db, cupom_id=cupom_id, cupom=cupom)

@app.get("/cupons/", response_model=list[CupomSchema.Cupom], tags=["Cupons"])
async def get_cupons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return CupomController.get_cupom(db, skip=skip, limit=limit)

@app.delete("/cupom/{cupom_id}", response_model=CupomSchema.Cupom, tags=["Cupons"])
async def delete_cupom(cupom_id: int, db: Session = Depends(get_db)):
    return CupomController.delete_cupom(db, cupom_id=cupom_id)

@app.get("/vendas/", response_model=list[VendaSchema.Venda], tags=["Vendas"])
async def get_vendas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return VendaController.get_venda(db, skip=skip, limit=limit)

@app.get("/vendas/produtos", response_model=list[VendaSchema.VendaProdutos], tags=["Vendas"])
async def get_venda_produtos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vendas_produtos = VendaController.get_venda_produtos(db, skip=skip, limit=limit)
    return vendas_produtos

@app.post("/venda", response_model=VendaSchema.VendaProdutos, tags=["Vendas"])
async def create_venda(venda: VendaSchema.VendaCreate, db: Session = Depends(get_db)):
    return VendaController.create_venda(db, venda=venda)


@app.get("/cupom_fiscal/{venda_id}", response_class=HTMLResponse, tags=["Vendas"])
async def generate_cupom_fiscal(venda_id: int, request: Request, db: Session = Depends(get_db)):
    venda_produtos = VendaController.get_venda_produtos_by_id(db, venda_id=venda_id)

    print(venda_produtos.sub_total)
    print(venda_produtos.total)
    print(venda_produtos.venda_produto)

    contexto = {
        "request": request,
        "venda": venda_produtos,
        "produtos": venda_produtos.venda_produto

    }

    return templates.TemplateResponse("index.html", contexto)

@app.get("/relatorio/vendas", tags=["Relatórios"])
async def relatorio_vendas(db: Session = Depends(get_db)):
    return VendaController.get_relatorio_vendas(db)

@app.get("/relatorio/estoque", tags=["Relatórios"])
async def relatorio_estoque(db: Session = Depends(get_db)):
    return ProdutoController.get_relatorio_estoque(db)

@app.get("/relatorio/movimentacoes/estoque", tags=["Relatórios"])
async def relatorio_movimentacoes_estoque(db: Session = Depends(get_db)):
    return ProdutoController.get_relatorio_movimentacoes_estoque(db)