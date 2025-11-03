#!/bin/bash
# Quick build and run script for KnightFight Bot

set -e  # Exit on error

echo "🐳 KnightFight Bot - Docker Quick Start"
echo "========================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado!"
    echo "   Instale: curl -fsSL https://get.docker.com | sh"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado!"
    echo "   Instale: sudo apt-get install docker-compose"
    exit 1
fi

echo "✅ Docker detectado: $(docker --version)"
echo "✅ Docker Compose detectado: $(docker-compose --version)"
echo ""

# Create data directories if they don't exist
echo "📁 Criando diretórios de dados..."
mkdir -p bot_data bot_screenshots
echo "✅ Diretórios criados"
echo ""

# Build Docker image
echo "🔨 Building Docker image..."
docker-compose build

if [ $? -eq 0 ]; then
    echo "✅ Build concluído com sucesso!"
else
    echo "❌ Build falhou!"
    exit 1
fi

echo ""
echo "========================================"
echo "🎉 Pronto para uso!"
echo "========================================"
echo ""
echo "Comandos disponíveis:"
echo ""
echo "  Iniciar bot:     docker-compose up -d"
echo "  Ver logs:        docker-compose logs -f"
echo "  Parar bot:       docker-compose down"
echo "  Reiniciar bot:   docker-compose restart"
echo "  Ver status:      docker-compose ps"
echo ""
echo "Iniciar agora? (y/n)"
read -r response

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo ""
    echo "🚀 Iniciando bot..."
    docker-compose up -d
    
    echo ""
    echo "✅ Bot iniciado!"
    echo ""
    echo "Ver logs em tempo real:"
    echo "  docker-compose logs -f"
    echo ""
    echo "Mostrando logs (Ctrl+C para sair)..."
    sleep 2
    docker-compose logs -f
else
    echo ""
    echo "👍 OK! Execute 'docker-compose up -d' quando quiser iniciar"
fi
