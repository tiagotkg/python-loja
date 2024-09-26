
from sqlalchemy import Column, Integer, String, DateTime, REAL
from sqlalchemy.orm import relationship
from database import Base

# definindo nossas models é praticamente nossas tabelas no banco de dados


# user que será utilizada para acesso ao sistema
class Venda(Base):
    __tablename__ = "venda"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    data        = Column(DateTime, nullable=False)
    sub_total   = Column(REAL, nullable=False)
    cupom_id    = Column(Integer, nullable=True)
    desconto    = Column(REAL, nullable=True)
    total       = Column(REAL, nullable=False)


    venda_produto = relationship("VendaProduto", back_populates="venda")