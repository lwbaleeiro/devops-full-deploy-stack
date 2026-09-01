#!/bin/bash
set -e

echo "==============================================="
echo "🚀 Iniciando ambiente DevOps Local Stack"
echo "==============================================="
echo "Construindo imagens e subindo containers (Emuladores + Aplicações)..."

cd acme-infra
docker-compose up -d --build

echo "==============================================="
echo "✅ Ambiente iniciado com sucesso!"
echo "==============================================="
echo "🌐 Frontend (Interface Web): http://localhost:8080"
echo "📡 Backend (Swagger API):    http://localhost:8000/docs"
echo "🐰 RabbitMQ (Admin):         http://localhost:15672 (admin/admin)"
echo "☁️  Floci-UI (Azure Mock):    http://localhost:4500"
echo "==============================================="
