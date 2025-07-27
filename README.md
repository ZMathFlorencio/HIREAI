# API CRUD de Vagas - FastAPI

Esta é uma API CRUD completa para gerenciar vagas de candidato, desenvolvida com FastAPI, SQLAlchemy e SQLite.

## Funcionalidades

- ✅ Criar vaga
- ✅ Listar todas as vagas
- ✅ Buscar vaga por ID
- ✅ Atualizar vaga
- ✅ Deletar vaga
- ✅ Status da aplicação

## Propriedades da Vaga

- **Nome da vaga**: Título da posição
- **Descrição**: Detalhes sobre a vaga
- **Criado em**: Data e hora de criação
- **Vaga disponível**: Status de disponibilidade (true/false)

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## Instalação e Configuração

### Opção 1: Usando Docker (Recomendado)

#### 1. Clone ou baixe o projeto
```bash
# Se estiver usando git
git clone <url-do-repositorio>
cd cursor_willm
```

#### 2. Executar com Docker Compose
```bash
# Construir e executar a aplicação
docker-compose up --build

# Executar em background
docker-compose up -d --build

# Parar a aplicação
docker-compose down
```

#### 3. Ou usar Docker diretamente
```bash
# Construir a imagem
docker build -t api-vagas .

# Executar o container
docker run -p 8000:8000 api-vagas
```

### Opção 2: Instalação Local

#### 1. Clone ou baixe o projeto
```bash
# Se estiver usando git
git clone <url-do-repositorio>
cd cursor_willm
```

#### 2. Criar ambiente virtual
```bash
# Windows (PowerShell)
python -m venv venv

# Ativar o ambiente virtual
venv\Scripts\Activate.ps1
```

#### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

#### 4. Executar a aplicação
```bash
# Desenvolvimento
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Produção
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 5. Acessar a aplicação
- **API**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **Documentação ReDoc**: http://localhost:8000/redoc

## Rotas da API

### 1. Status da Aplicação
- **GET** `/` - Verifica se a aplicação está online

### 2. CRUD de Vagas
- **POST** `/vagas/` - Criar nova vaga
- **GET** `/vagas/` - Listar todas as vagas
- **GET** `/vagas/{vaga_id}` - Buscar vaga por ID
- **PUT** `/vagas/{vaga_id}` - Atualizar vaga
- **DELETE** `/vagas/{vaga_id}` - Deletar vaga

## Exemplos de Uso

### Criar uma vaga
```bash
curl -X POST "http://localhost:8000/vagas/" \
     -H "Content-Type: application/json" \
     -d '{
       "nome": "Desenvolvedor Python",
       "descricao": "Vaga para desenvolvedor Python com experiência em FastAPI",
       "vaga_disponivel": true
     }'
```

### Listar todas as vagas
```bash
curl -X GET "http://localhost:8000/vagas/"
```

### Buscar vaga por ID
```bash
curl -X GET "http://localhost:8000/vagas/1"
```

### Atualizar vaga
```bash
curl -X PUT "http://localhost:8000/vagas/1" \
     -H "Content-Type: application/json" \
     -d '{
       "nome": "Desenvolvedor Python Senior",
       "descricao": "Vaga para desenvolvedor Python senior com experiência em FastAPI",
       "vaga_disponivel": false
     }'
```

### Deletar vaga
```bash
curl -X DELETE "http://localhost:8000/vagas/1"
```

## Executar Testes

```bash
# Executar todos os testes
pytest

# Executar testes com detalhes
pytest -v

# Executar testes com cobertura
pytest --cov=app tests/
```

## Estrutura do Projeto

```
cursor_willm/
├── app/
│   ├── __init__.py
│   ├── models.py          # Modelos SQLAlchemy
│   ├── schemas.py         # Schemas Pydantic
│   ├── database.py        # Configuração do banco
│   └── crud.py           # Operações CRUD
├── tests/
│   ├── __init__.py
│   └── test_api.py       # Testes da API
├── main.py               # Aplicação principal
├── requirements.txt      # Dependências
└── README.md            # Este arquivo
```

## Banco de Dados

- **Tipo**: SQLite
- **Arquivo**: `vagas.db` (criado automaticamente)
- **ORM**: SQLAlchemy

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para Python
- **Pydantic**: Validação de dados
- **SQLite**: Banco de dados
- **Pytest**: Framework de testes
- **Uvicorn**: Servidor ASGI
- **Docker**: Containerização da aplicação

## Desenvolvimento

Para desenvolvimento local, a aplicação usa o modo de recarga automática:
```bash
uvicorn main:app --reload
```

Isso permite que as mudanças no código sejam aplicadas automaticamente sem reiniciar o servidor.

## Docker

### Comandos Úteis

```bash
# Construir imagem
docker build -t api-vagas .

# Executar container
docker run -p 8000:8000 api-vagas

# Executar em modo interativo
docker run -it -p 8000:8000 api-vagas /bin/bash

# Ver logs do container
docker logs <container_id>

# Parar container
docker stop <container_id>

# Remover container
docker rm <container_id>

# Remover imagem
docker rmi api-vagas
```

### Docker Compose

```bash
# Construir e executar
docker-compose up --build

# Executar em background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar serviços
docker-compose down

# Reconstruir sem cache
docker-compose build --no-cache
```

### Volumes

O banco de dados SQLite é persistido através de um volume Docker, garantindo que os dados não sejam perdidos quando o container for reiniciado. 