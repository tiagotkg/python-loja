
from sqlalchemy import Column, Integer, String, REAL
from sqlalchemy.orm import relationship
from database import Base

# definindo nossas models é praticamente nossas tabelas no banco de dados


# user que será utilizada para acesso ao sistema
class Produto(Base):
    __tablename__ = "produto"

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    nome                = Column(String, nullable=False)
    codigo              = Column(String, unique=True, nullable=False)
    categoria           = Column(String, nullable=False)
    quantidade          = Column(Integer, nullable=False, default=0)
    quantidade_minima   = Column(Integer, nullable=False)
    preco               = Column(REAL, nullable=False)
    preco_promocional   = Column(REAL, nullable=True)
    descricao           = Column(String, default=False)
    fornecedor          = Column(String, default=False)

    estoque = relationship("Estoque", back_populates="produto")