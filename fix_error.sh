#!/bin/bash

echo "🔧 Resolvendo problema de compatibilidade Python 3.11..."

# Parar containers em execução
echo "🛑 Parando containers..."
docker-compose down 2>/dev/null || true

# Limpar cache e imagens antigas
echo "🧹 Limpando cache..."
docker system prune -f
docker builder prune -f

# Remover imagens antigas
echo "🗑️ Removendo imagens antigas..."
docker rmi $(docker images -q api-vagas) 2>/dev/null || true

# Construir com Dockerfile simples (Python 3.10)
echo "🏗️ Construindo com Python 3.10..."
docker-compose build --no-cache

# Testar a aplicação
echo "🧪 Testando aplicação..."
docker-compose up -d

# Aguardar aplicação inicializar
echo "⏳ Aguardando aplicação inicializar..."
sleep 10

# Testar endpoint
echo "🔍 Testando endpoint..."
if curl -f http://localhost:8000/ > /dev/null 2>&1; then
    echo "✅ Aplicação funcionando corretamente!"
    echo "🌐 Acesse: http://localhost:8000"
    echo "📚 Documentação: http://localhost:8000/docs"
else
    echo "❌ Aplicação não está respondendo"
    echo "📋 Verificando logs..."
    docker-compose logs api
fi

echo ""
echo "📋 Comandos úteis:"
echo "  - Ver logs: docker-compose logs -f"
echo "  - Parar: docker-compose down"
echo "  - Rebuild: docker-compose up --build" 