from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.database import engine, get_db

# Criar tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

# Criar aplicação FastAPI
app = FastAPI(
    title="API CRUD de Vagas",
    description="API para gerenciar vagas de candidato com FastAPI e SQLAlchemy",
    version="1.0.0"
)

@app.get("/")
def read_root():
    """Rota inicial para verificar se a aplicação está online"""
    return {
        "message": "API CRUD de Vagas está online!",
        "status": "success",
        "docs": "/docs",
        "redoc": "/redoc",
        "matheus": "/swagger"
    }

@app.post("/vagas/", response_model=schemas.Vaga, status_code=201)
def create_vaga(vaga: schemas.VagaCreate, db: Session = Depends(get_db)):
    """Criar uma nova vaga"""
    return crud.create_vaga(db=db, vaga=vaga)

@app.get("/vagas/", response_model=List[schemas.Vaga])
def read_vagas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todas as vagas"""
    vagas = crud.get_vagas(db, skip=skip, limit=limit)
    return vagas

@app.get("/vagas/publico/{slug}", response_model=schemas.Vaga)
def read_vaga_publica(slug: str, db: Session = Depends(get_db)):
    """Buscar uma vaga por SLUG (acesso público)"""
    vaga = db.query(models.Vaga).filter(models.Vaga.slug == slug).first()
    if not vaga:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return vaga

@app.get("/teste-conexao")#teste de conexão com o banco de dados
def teste_conexao(db: Session = Depends(get_db)):
    try:
        # Apenas tenta realizar uma operação simples no banco
        db.execute("SELECT 1")
        return {"status": "Conexão com o banco funcionando"}
    except Exception as e:
        return {"erro": str(e)}


@app.get("/vagas/{vaga_id}", response_model=schemas.Vaga)
def read_vaga(vaga_id: int, db: Session = Depends(get_db)):
    """Buscar uma vaga específica por ID"""
    db_vaga = crud.get_vaga(db, vaga_id=vaga_id)
    if db_vaga is None:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return db_vaga

@app.put("/vagas/{vaga_id}", response_model=schemas.Vaga)
def update_vaga(vaga_id: int, vaga: schemas.VagaUpdate, db: Session = Depends(get_db)):
    """Atualizar uma vaga existente"""
    db_vaga = crud.update_vaga(db, vaga_id=vaga_id, vaga=vaga)
    if db_vaga is None:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return db_vaga

@app.delete("/vagas/{vaga_id}")
def delete_vaga(vaga_id: int, db: Session = Depends(get_db)):
    """Deletar uma vaga"""
    success = crud.delete_vaga(db, vaga_id=vaga_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return {"message": "Vaga deletada com sucesso"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 