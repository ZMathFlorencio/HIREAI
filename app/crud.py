import random
import string
from unidecode import unidecode

def gerar_slug(nome: str):
    """Gera um slug legível e único a partir do nome da vaga"""
    nome_normalizado = unidecode(nome.lower().replace(" ", "-"))
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
    """Criar nova vaga com slug automático"""
    slug = gerar_slug(vaga.nome)
    db_vaga = models.Vaga(**vaga.dict(), slug=slug)
    db.add(db_vaga)
    db.commit()
    db.refresh(db_vaga)
    return db_vaga

def update_vaga(db: Session, vaga_id: int, vaga: schemas.VagaUpdate):
    """Atualizar vaga existente"""
    db_vaga = db.query(models.Vaga).filter(models.Vaga.id == vaga_id).first()
    if db_vaga:
        update_data = vaga.dict(exclude_unset=True)
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