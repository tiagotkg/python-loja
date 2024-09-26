
from sqlalchemy import Column, Integer, String, DateTime, REAL, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# definindo nossas models é praticamente nossas tabelas no banco de dados


# user que será utilizada para acesso ao sistema
class VendaProduto(Base):
    __tablename__ = "venda_produto"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    venda_id    = Column(Integer, ForeignKey("venda.id"), nullable= False)
    produto_id  = Column(Integer, ForeignKey("produto.id"), nullable= False)
    quantidade  = Column(Integer, nullable=False)
    valor       = Column(REAL, nullable=False)

    venda   = relationship("Venda", back_populates="venda_produto")
    produto   = relationship("Produto", back_populates="venda_produto")