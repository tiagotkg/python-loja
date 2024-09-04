import datetime

from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from database import Base

# definindo nossas models é praticamente nossas tabelas no banco de dados


# user que será utilizada para acesso ao sistema
class Estoque(Base):
    __tablename__ = "estoque"

    id = Column(Integer, primary_key=True, autoincrement=True)
    produto_id = Column(Integer,nullable=False)
    quantidade_minima = Column(Integer, nullable=False)
    quantidade = Column(Integer, nullable=False)
    quantidade_maxima = Column(Integer, nullable=False)

    produto = relationship("Produto", back_populates="owner")