from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException

from controller.EstoqueController import create_estoque
from model.Cupom import Cupom
from model.Venda import Venda
from model.Produto import Produto
from model.VendaProduto import VendaProduto
import schema
from sqlalchemy.sql.operators import and_

from schema.EstoqueSchema import EstoqueCreate
from fastapi.responses import StreamingResponse
import pandas as pd
import io

def get_venda(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Venda).offset(skip).limit(limit).all()


def get_venda_produtos(db: Session, skip: int = 0, limit: int = 100):
    venda_produtos = db.query(Venda).options(joinedload(Venda.venda_produto).joinedload(VendaProduto.produto)).offset(skip).limit(limit).all()
    return venda_produtos

def get_venda_produtos_by_id(db: Session, venda_id):
    venda_produtos = db.query(Venda).options(joinedload(Venda.venda_produto).joinedload(VendaProduto.produto)).filter(Venda.id == venda_id).first()
    return venda_produtos


def get_venda_estoque_alerta(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Venda).options(joinedload(Venda.estoque)).filter(Venda.quantidade <= Venda.quantidade_minima).all()

def create_venda(db: Session, venda: schema.VendaSchema.VendaCreate):

    cupom_id = None
    desconto = 0
    subtotal = 0

    # validação dos produtos
    for produto in venda.produtos:
        db_produto = db.query(Produto).options(joinedload(Produto.estoque)).filter(Produto.id == produto.produto_id).first()

        if db_produto is None:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        if db_produto.quantidade < produto.quantidade:
            raise HTTPException(status_code=404, detail="Quantidade indisponível")

        subtotal = subtotal + (db_produto.preco_promocional * produto.quantidade)

    # validação do cupom
    if venda.cupom:
        db_cupom = db.query(Cupom).filter(and_(Cupom.codigo == venda.cupom, Cupom.deleted_at == None)).first();

        if db_cupom is None:
            raise HTTPException(status_code=404, detail="Cupom não encontrado")

        cupom_id = db_cupom.id

        if db_cupom.porcentagem:
            desconto = subtotal * db_cupom.valor / 100
        else:
            desconto = db_cupom.valor


    total = subtotal - desconto


    # criando venda
    db_venda = Venda(data=func.now(), total=total, sub_total=subtotal, desconto=desconto, cupom_id=cupom_id)
    db.add(db_venda)
    db.commit()
    db.refresh(db_venda)

    # inserido registros dos produtos
    venda_produtos = []
    for produto in venda.produtos:
        db_produto = db.query(Produto).options(joinedload(Produto.estoque)).filter(Produto.id == produto.produto_id).first()

        print(db_produto.id)

        db_venda_produto = db_produto = VendaProduto(venda_id=db_venda.id, produto_id=db_produto.id, quantidade=produto.quantidade, valor=db_produto.preco)
        db.add(db_venda_produto)
        db.commit()

        venda_produtos.append(db_venda_produto)
        db_estoque = EstoqueCreate(produto_id=produto.produto_id ,quantidade=produto.quantidade)
        create_estoque(db, db_estoque, False)


    db.refresh(db_venda_produto)

    db_venda.produtos = venda_produtos
    return db_venda


def update_venda(db: Session, venda_id: int, venda: schema.VendaSchema.VendaUpdate):
    db_venda = db.query(Venda).filter(Venda.id == venda_id).first()
    if db_venda is None:
        raise HTTPException(status_code=404, detail="Venda não encontrado")

    for key, value in venda.model_dump().items():
        if(value):
            setattr(db_venda, key, value)

    db.commit()
    db.refresh(db_venda)
    return db_venda


def get_relatorio_vendas(db: Session):
    vendas_produtos = get_venda_produtos(db)

    venda = []
    for venda_produto in vendas_produtos:
        for produto in venda_produto.venda_produto:
            venda.append({
                "venda_id": venda_produto.id,
                "data_venda": venda_produto.data,
                "produto": produto.produto.nome, "quantidade": produto.quantidade,
                "valor": produto.valor, "valor_promocional": produto.produto.preco_promocional,
                "sub_total": venda_produto.sub_total, "desconto": venda_produto.desconto,
                "total": venda_produto.total
            })

    df = pd.DataFrame(venda)

    # Cria um buffer em memória para o arquivo Excel
    output = io.BytesIO()

    # Escreve o DataFrame no buffer como um arquivo Excel
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Relatório')

    # Posiciona o cursor no início do buffer
    output.seek(0)

    # Define os headers para o download do arquivo
    headers = {'Content-Disposition': 'attachment; filename="relatorio_vendas.xlsx"'}

    # Retorna o arquivo como uma resposta de streaming
    return StreamingResponse(output, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers=headers)

