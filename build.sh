#!/bin/bash

echo "🔨 Construindo imagem Docker para API de Vagas..."

# Remover containers e imagens antigas (opcional)
echo "🧹 Limpando containers e imagens antigas..."
docker-compose down
docker system prune -f

# Construir a imagem
echo "🏗️ Construindo nova imagem..."
docker-compose build --no-cache

# Executar a aplicação
echo "🚀 Iniciando a aplicação..."
docker-compose up -d

echo "✅ Build concluído!"
echo "🌐 Aplicação disponível em: http://localhost:8000"
echo "📚 Documentação em: http://localhost:8000/docs"
echo ""
echo "📋 Comandos úteis:"
echo "  - Ver logs: docker-compose logs -f"
echo "  - Parar: docker-compose down"
echo "  - Rebuild: docker-compose up --build" 