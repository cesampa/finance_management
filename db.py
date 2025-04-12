from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_MODE, SQLITE_URL, POSTGRES_URL

Base = declarative_base()

class Lancamento(Base):
    __tablename__ = 'lancamentos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, nullable=False)
    descricao = Column(String(255), nullable=False)
    valor = Column(Float, nullable=False)
    comentarios = Column(Text, nullable=True)
    saldo = Column(Float, nullable=False)

def get_engine():
    db_url = SQLITE_URL if DB_MODE == "sqlite" else POSTGRES_URL
    return create_engine(db_url, echo=False)

def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()
