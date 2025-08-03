from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

# ===== SCHEMAS PARA VAGA =====

# Schema base para vaga
class VagaBase(BaseModel):
    nome_vaga: str
    desc_vaga: str
    modelo_trab: str
    modelo_cont: str
    slug: str

# Schema para criar vaga
class VagaCreate(VagaBase):
    pass

# Schema para atualizar vaga
class VagaUpdate(BaseModel):
    nome_vaga: Optional[str] = None
    desc_vaga: Optional[str] = None
    modelo_trab: Optional[str] = None
    modelo_cont: Optional[str] = None
    slug: Optional[str] = None

# Schema para resposta da vaga
class Vaga(VagaBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# ===== SCHEMAS PARA CANDIDATO =====

# Schema base para candidato
class CandidatoBase(BaseModel):
    nome_completo: str
    telefone: str
    email: str
    skill: str
    video: str
    transcricao: str
    Perfil: str
    video_url: str
    vaga_id: int

# Schema para criar candidato
class CandidatoCreate(CandidatoBase):
    pass

# Schema para atualizar candidato
class CandidatoUpdate(BaseModel):
    nome_completo: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    skill: Optional[str] = None
    video: Optional[str] = None
    transcricao: Optional[str] = None
    Perfil: Optional[str] = None
    video_url: Optional[str] = None
    vaga_id: Optional[int] = None

# Schema para resposta do candidato
class Candidato(CandidatoBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# ===== SCHEMAS COM RELACIONAMENTOS =====

# Vaga com lista de candidatos
class VagaComCandidatos(Vaga):
    candidatos: List[Candidato] = []

# Candidato com informações da vaga
class CandidatoComVaga(Candidato):
    vaga: Vaga
