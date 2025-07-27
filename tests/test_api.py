import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from app.database import get_db
from app.models import Base

# Criar banco de dados de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar tabelas de teste
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestAPI:
    """Testes para a API CRUD de Vagas"""

    def test_read_root(self):
        """Teste da rota inicial"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "API CRUD de Vagas está online!"
        assert data["status"] == "success"

    def test_create_vaga(self):
        """Teste de criação de vaga"""
        vaga_data = {
            "nome": "Desenvolvedor Python",
            "descricao": "Vaga para desenvolvedor Python com experiência em FastAPI",
            "vaga_disponivel": True
        }
        response = client.post("/vagas/", json=vaga_data)
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == vaga_data["nome"]
        assert data["descricao"] == vaga_data["descricao"]
        assert data["vaga_disponivel"] == vaga_data["vaga_disponivel"]
        assert "id" in data
        assert "criado_em" in data

    def test_read_vagas(self):
        """Teste de listagem de vagas"""
        # Criar algumas vagas primeiro
        vagas_data = [
            {
                "nome": "Desenvolvedor Frontend",
                "descricao": "Vaga para desenvolvedor Frontend",
                "vaga_disponivel": True
            },
            {
                "nome": "Desenvolvedor Backend",
                "descricao": "Vaga para desenvolvedor Backend",
                "vaga_disponivel": False
            }
        ]
        
        for vaga_data in vagas_data:
            client.post("/vagas/", json=vaga_data)

        response = client.get("/vagas/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2

    def test_read_vaga(self):
        """Teste de busca de vaga por ID"""
        # Criar uma vaga
        vaga_data = {
            "nome": "Desenvolvedor Full Stack",
            "descricao": "Vaga para desenvolvedor Full Stack",
            "vaga_disponivel": True
        }
        create_response = client.post("/vagas/", json=vaga_data)
        vaga_id = create_response.json()["id"]

        # Buscar a vaga criada
        response = client.get(f"/vagas/{vaga_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == vaga_id
        assert data["nome"] == vaga_data["nome"]

    def test_read_vaga_not_found(self):
        """Teste de busca de vaga inexistente"""
        response = client.get("/vagas/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Vaga não encontrada"

    def test_update_vaga(self):
        """Teste de atualização de vaga"""
        # Criar uma vaga
        vaga_data = {
            "nome": "Desenvolvedor Junior",
            "descricao": "Vaga para desenvolvedor Junior",
            "vaga_disponivel": True
        }
        create_response = client.post("/vagas/", json=vaga_data)
        vaga_id = create_response.json()["id"]

        # Atualizar a vaga
        update_data = {
            "nome": "Desenvolvedor Pleno",
            "vaga_disponivel": False
        }
        response = client.put(f"/vagas/{vaga_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == update_data["nome"]
        assert data["vaga_disponivel"] == update_data["vaga_disponivel"]
        assert data["descricao"] == vaga_data["descricao"]  # Não deve ter mudado

    def test_update_vaga_not_found(self):
        """Teste de atualização de vaga inexistente"""
        update_data = {
            "nome": "Vaga Atualizada",
            "vaga_disponivel": False
        }
        response = client.put("/vagas/999", json=update_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "Vaga não encontrada"

    def test_delete_vaga(self):
        """Teste de exclusão de vaga"""
        # Criar uma vaga
        vaga_data = {
            "nome": "Vaga para Deletar",
            "descricao": "Esta vaga será deletada",
            "vaga_disponivel": True
        }
        create_response = client.post("/vagas/", json=vaga_data)
        vaga_id = create_response.json()["id"]

        # Deletar a vaga
        response = client.delete(f"/vagas/{vaga_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Vaga deletada com sucesso"

        # Verificar se a vaga foi realmente deletada
        get_response = client.get(f"/vagas/{vaga_id}")
        assert get_response.status_code == 404

    def test_delete_vaga_not_found(self):
        """Teste de exclusão de vaga inexistente"""
        response = client.delete("/vagas/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Vaga não encontrada"

    def test_create_vaga_validation(self):
        """Teste de validação de dados na criação"""
        # Teste sem nome (campo obrigatório)
        vaga_data = {
            "descricao": "Vaga sem nome",
            "vaga_disponivel": True
        }
        response = client.post("/vagas/", json=vaga_data)
        assert response.status_code == 422

        # Teste sem descrição (campo obrigatório)
        vaga_data = {
            "nome": "Vaga sem descrição",
            "vaga_disponivel": True
        }
        response = client.post("/vagas/", json=vaga_data)
        assert response.status_code == 422

    def test_pagination(self):
        """Teste de paginação na listagem"""
        # Criar mais vagas para testar paginação
        for i in range(5):
            vaga_data = {
                "nome": f"Vaga {i+1}",
                "descricao": f"Descrição da vaga {i+1}",
                "vaga_disponivel": True
            }
            client.post("/vagas/", json=vaga_data)

        # Testar limite
        response = client.get("/vagas/?limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 3

        # Testar offset
        response = client.get("/vagas/?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 2 