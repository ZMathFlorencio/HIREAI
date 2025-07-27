#!/usr/bin/env python3
"""
Script de teste para verificar se a aplicação FastAPI está funcionando
"""

import sys
import subprocess
import time
import requests

def test_imports():
    """Testa se as importações funcionam"""
    print("🔍 Testando importações...")
    
    try:
        import fastapi
        print("✅ FastAPI importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar FastAPI: {e}")
        return False
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar SQLAlchemy: {e}")
        return False
    
    try:
        import pydantic
        print("✅ Pydantic importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar Pydantic: {e}")
        return False
    
    return True

def test_app_creation():
    """Testa se a aplicação pode ser criada"""
    print("\n🔍 Testando criação da aplicação...")
    
    try:
        from main import app
        print("✅ Aplicação criada com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar aplicação: {e}")
        return False

def test_endpoints():
    """Testa os endpoints da aplicação"""
    print("\n🔍 Testando endpoints...")
    
    try:
        from main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Teste do endpoint raiz
        response = client.get("/")
        if response.status_code == 200:
            print("✅ Endpoint raiz funcionando")
        else:
            print(f"❌ Endpoint raiz falhou: {response.status_code}")
            return False
        
        # Teste de criação de vaga
        vaga_data = {
            "nome": "Teste",
            "descricao": "Vaga de teste",
            "vaga_disponivel": True
        }
        response = client.post("/vagas/", json=vaga_data)
        if response.status_code == 201:
            print("✅ Endpoint de criação funcionando")
        else:
            print(f"❌ Endpoint de criação falhou: {response.status_code}")
            return False
        
        # Teste de listagem
        response = client.get("/vagas/")
        if response.status_code == 200:
            print("✅ Endpoint de listagem funcionando")
        else:
            print(f"❌ Endpoint de listagem falhou: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar endpoints: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Iniciando testes da aplicação FastAPI\n")
    
    # Teste 1: Importações
    if not test_imports():
        print("\n❌ Falha nos testes de importação")
        sys.exit(1)
    
    # Teste 2: Criação da aplicação
    if not test_app_creation():
        print("\n❌ Falha na criação da aplicação")
        sys.exit(1)
    
    # Teste 3: Endpoints
    if not test_endpoints():
        print("\n❌ Falha nos testes de endpoints")
        sys.exit(1)
    
    print("\n🎉 Todos os testes passaram! A aplicação está funcionando corretamente.")
    print("\n📋 Para executar a aplicação:")
    print("   - Local: uvicorn main:app --reload")
    print("   - Docker: docker-compose up --build")

if __name__ == "__main__":
    main() 