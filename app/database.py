import os  # Biblioteca padrão do Python para acessar variáveis de ambiente
from sqlalchemy import create_engine  # Cria o motor de conexão com o banco
from sqlalchemy.ext.declarative import declarative_base  # Base para os modelos de dados
from sqlalchemy.orm import sessionmaker  # Gerencia sessões com o banco (para consultas, inserções etc.)

# ▶️ Pega a URL de conexão do banco de dados da variável de ambiente DATABASE_URL
# Essa variável será configurada no Railway com a string de conexão do Supabase
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 🔌 Cria o engine de conexão com o banco
# Esse engine é usado internamente pelo SQLAlchemy para enviar comandos SQL ao banco
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 💬 Cria uma fábrica de sessões (SessionLocal)
# Cada vez que você chamar get_db(), uma nova sessão será criada com essas configurações
SessionLocal = sessionmaker(
    autocommit=False,  # Desliga o commit automático (você controla quando salvar)
    autoflush=False,   # Não envia mudanças para o banco automaticamente antes do commit
    bind=engine        # Usa o engine definido acima
)

# 📦 Base de onde todos os modelos irão herdar (ex: Vaga, Candidato)
# Isso permite que o SQLAlchemy saiba como criar as tabelas no banco a partir dos modelos
Base = declarative_base()

# 🔁 Função que será usada nas rotas para abrir uma sessão com o banco
# O `yield` permite usar essa função como dependência no FastAPI e garante que a sessão seja fechada no final
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()