import datetime

from sqlalchemy import Column, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship
from database import Base

# definindo nossas models é praticamente nossas tabelas no banco de dados


# user que será utilizada para acesso ao sistema
class Estoque(Base):
    __tablename__ = "estoque"

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    quantidade          = Column(Integer, nullable=False)
    entrada_saida       = Column(Boolean, nullable=False)
    produto_id          = Column(Integer, ForeignKey("produto.id"), nullable= False)

    produto = relationship("Produto", back_populates="estoque")
