# Web Backend API

Esta é uma API FastAPI para gerenciar eventos. Ela serve como backend para a aplicação frontend e se conecta aos recursos de infraestrutura provisionados via Terraform.

## Dependências Simuladas
- **CosmosDB**: Armazenamento de dados principal.
- **Redis**: Cache para leitura rápida.
- **RabbitMQ / EventHub**: Mensageria assíncrona para publicação de eventos.
- **Blob Storage**: Armazenamento de anexos.

As conexões são feitas de forma segura usando variáveis de ambiente que, em um ambiente real, seriam injetadas como Secrets a partir do Azure Key Vault via ArgoCD/Kubernetes.

## Rodando Localmente (Requer Python)
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Docker
```bash
docker build -t web-backend .
docker run -p 8000:8000 web-backend
```
