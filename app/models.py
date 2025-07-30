from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base

class Vaga(Base):
    __tablename__ = "vagas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    descricao = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)  # <- AQUI
    criado_em = Column(DateTime, server_default=func.now())
    vaga_disponivel = Column(Boolean, default=True)