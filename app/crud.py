import random
import string
import unicodedata

def gerar_slug(nome: str):
    """Gera um slug legível e único a partir do nome da vaga"""
    # Remove acentos usando unicodedata (biblioteca padrão do Python)
    nome_sem_acentos = ''.join(c for c in unicodedata.normalize('NFD', nome.lower())
                              if not unicodedata.combining(c))
    nome_normalizado = nome_sem_acentos.replace(" ", "-")
    sufixo = ''.join(random.choices(string.digits, k=4))
    return f"{nome_normalizado}-{sufixo}"

from sqlalchemy.orm import Session
from . import models, schemas

def get_vaga(db: Session, vaga_id: int):
    """Buscar vaga por ID"""
    return db.query(models.Vaga).filter(models.Vaga.id == vaga_id).first()

def get_vagas(db: Session, skip: int = 0, limit: int = 100):
    """Listar todas as vagas com paginação"""
    return db.query(models.Vaga).offset(skip).limit(limit).all()

def create_vaga(db: Session, vaga: schemas.VagaCreate):
    """Criar nova vaga"""
    db_vaga = models.Vaga(**vaga.model_dump())
    db.add(db_vaga)
    db.commit()
    db.refresh(db_vaga)
    return db_vaga

def update_vaga(db: Session, vaga_id: int, vaga: schemas.VagaUpdate):
    """Atualizar vaga existente"""
    db_vaga = db.query(models.Vaga).filter(models.Vaga.id == vaga_id).first()
    if db_vaga:
        update_data = vaga.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_vaga, field, value)
        db.commit()
        db.refresh(db_vaga)
    return db_vaga

def delete_vaga(db: Session, vaga_id: int):
    """Deletar vaga"""
    db_vaga = db.query(models.Vaga).filter(models.Vaga.id == vaga_id).first()
    if db_vaga:
        db.delete(db_vaga)
        db.commit()
        return True
    return False

# ===== FUNÇÕES CRUD PARA CANDIDATOS =====

def get_candidato(db: Session, candidato_id: int):
    """Buscar candidato por ID"""
    return db.query(models.Candidato).filter(models.Candidato.id == candidato_id).first()

def get_candidatos(db: Session, skip: int = 0, limit: int = 100):
    """Listar todos os candidatos com paginação"""
    return db.query(models.Candidato).offset(skip).limit(limit).all()

def get_candidatos_por_vaga(db: Session, vaga_id: int, skip: int = 0, limit: int = 100):
    """Listar candidatos de uma vaga específica"""
    return db.query(models.Candidato).filter(models.Candidato.vaga_id == vaga_id).offset(skip).limit(limit).all()

def create_candidato(db: Session, candidato: schemas.CandidatoCreate):
    """Criar novo candidato"""
    db_candidato = models.Candidato(**candidato.model_dump())
    db.add(db_candidato)
    db.commit()
    db.refresh(db_candidato)
    return db_candidato

def update_candidato(db: Session, candidato_id: int, candidato: schemas.CandidatoUpdate):
    """Atualizar candidato existente"""
    db_candidato = db.query(models.Candidato).filter(models.Candidato.id == candidato_id).first()
    if db_candidato:
        update_data = candidato.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_candidato, field, value)
        db.commit()
        db.refresh(db_candidato)
    return db_candidato

def delete_candidato(db: Session, candidato_id: int):
    """Deletar candidato"""
    db_candidato = db.query(models.Candidato).filter(models.Candidato.id == candidato_id).first()
    if db_candidato:
        db.delete(db_candidato)
        db.commit()
        return True
    return False 