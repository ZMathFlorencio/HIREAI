from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schema base para vaga
class VagaBase(BaseModel):
    nome: str
    descricao: str
    vaga_disponivel: bool = True

# Schema para criar vaga
class VagaCreate(VagaBase):
    pass

# Schema para atualizar vaga
class VagaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    vaga_disponivel: Optional[bool] = None

# Schema para resposta da vaga
class Vaga(VagaBase):
    id: int
    slug: str               # <-- Adicionamos aqui
    criado_em: datetime

    class Config:
        orm_mode = True
