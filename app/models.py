from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Vaga(Base):
    __tablename__ = "vagas"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    nome_vaga = Column(String, nullable=False)
    desc_vaga = Column(Text, nullable=False)
    modelo_trab = Column(String, nullable=False)
    modelo_cont = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    
    # Relacionamento com candidatos
    candidatos = relationship("Candidato", back_populates="vaga")

class Candidato(Base):
    __tablename__ = "candidato"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    nome_completo = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    skill = Column(Text, nullable=False)
    video = Column(Text, nullable=False)
    transcricao = Column(Text, nullable=False)
    Perfil = Column(Text, nullable=False)
    video_url = Column(Text, nullable=False)
    vaga_id = Column(Integer, ForeignKey("vagas.id"), nullable=False)
    
    # Relacionamento com vaga
    vaga = relationship("Vaga", back_populates="candidatos")