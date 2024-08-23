from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# path do nosso banco de dados slqlite
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# criando a comunicação com nosso banco de dados
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# criando sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# criando base para herdarmos futuramente nas models
Base = declarative_base()