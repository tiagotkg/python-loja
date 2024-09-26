
from sqlalchemy import Column, Integer, String, Boolean, REAL, DateTime
from sqlalchemy.orm import relationship
from database import Base

# definindo nossas models é praticamente nossas tabelas no banco de dados


# user que será utilizada para acesso ao sistema
class Cupom(Base):
    __tablename__ = "cupom"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    codigo      = Column(String, nullable=False)
    porcentagem = Column(Boolean, nullable=False)
    valor       = Column(REAL, nullable=False)
    ativo       = Column(Boolean, nullable=False, default=True)
    deleted_at  = Column(DateTime, nullable=True)

    #venda = relationship("Venda", back_populates="cupom")