from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from model.Produto import Produto
import schema
from fastapi.responses import StreamingResponse
import pandas as pd
import io

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


def get_relatorio_estoque(db: Session):
    estoque_produtos = get_produto_estoque(db)

    relatorio = []
    for estoque_produto in estoque_produtos:
        relatorio.append({
            "produto_id": estoque_produto.id,
            "categoria": estoque_produto.categoria,
            "codigo": estoque_produto.codigo,
            "nome": estoque_produto.nome,
            "descricao": estoque_produto.descricao,
            "fornecedor": estoque_produto.fornecedor,
            "preco": estoque_produto.preco,
            "preco_promocional": estoque_produto.preco_promocional,
            "quantidade_minima": estoque_produto.quantidade_minima,
            "quantidade": estoque_produto.quantidade,
        })

    df = pd.DataFrame(relatorio)

    # Cria um buffer em memória para o arquivo Excel
    output = io.BytesIO()

    # Escreve o DataFrame no buffer como um arquivo Excel
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Relatório')

    # Posiciona o cursor no início do buffer
    output.seek(0)

    # Define os headers para o download do arquivo
    headers = {'Content-Disposition': 'attachment; filename="relatorio_estoque.xlsx"'}

    # Retorna o arquivo como uma resposta de streaming
    return StreamingResponse(output, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers=headers)


def get_relatorio_movimentacoes_estoque(db: Session):
    estoque_produtos = get_produto_estoque(db)

    relatorio = []
    for estoque_produto in estoque_produtos:
        for estoque in estoque_produto.estoque:

            entrada_saida = "saída"
            if estoque.entrada_saida:
                entrada_saida = "entrada"

            relatorio.append({
                "produto_id": estoque_produto.id,
                "codigo": estoque_produto.codigo,
                "nome": estoque_produto.nome,
                "quantidade": estoque.quantidade,
                "entrada_saida": entrada_saida,
            })

    df = pd.DataFrame(relatorio)

    # Cria um buffer em memória para o arquivo Excel
    output = io.BytesIO()

    # Escreve o DataFrame no buffer como um arquivo Excel
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Relatório')

    # Posiciona o cursor no início do buffer
    output.seek(0)

    # Define os headers para o download do arquivo
    headers = {'Content-Disposition': 'attachment; filename="relatorio_movimentacoes_estoque.xlsx"'}

    # Retorna o arquivo como uma resposta de streaming
    return StreamingResponse(output, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers=headers)

