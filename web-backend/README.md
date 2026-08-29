# Web Backend API

This is a FastAPI API for managing events. It serves as a backend for the frontend application and connects to the infrastructure resources provisioned via Terraform.

## Simulated Dependencies
- **CosmosDB**: Main data storage.
- **Redis**: Cache for fast reads.
- **RabbitMQ / EventHub**: Asynchronous messaging for event publishing.
- **Blob Storage**: Attachment storage.

Connections are made securely using environment variables which, in a real environment, would be injected as Secrets from Azure Key Vault via ArgoCD/Kubernetes.

## Running Locally (Requires Python)
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Docker
```bash
docker build -t web-backend .
docker run -p 8000:8000 web-backend
```
