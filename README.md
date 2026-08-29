# Projeto DevOps Full Deploy Stack

Este projeto simula uma arquitetura de nuvem corporativa com separação de responsabilidades entre times de Plataforma, Operações/GitOps e Produto.

## Diagrama da Arquitetura

O fluxo principal do provisionamento de recursos e gerenciamento de segredos funciona da seguinte forma:

1. **IaC Platform**: Provisiona recursos Azure (bancos, cache, etc.) e salva as credenciais no Key Vault do ambiente.
2. **GitOps Extensions**: Hospeda templates de `ExternalSecret`. O ArgoCD sincroniza esses templates no cluster K8s.
3. **ESO (External Secrets Operator)**: Lê o Key Vault usando as instruções do `ExternalSecret` e gera um Secret nativo no cluster.
4. **Workload (Aplicação)**: A aplicação é implantada pelo ArgoCD e simplesmente consome o Secret nativo injetado como variáveis de ambiente.

## Repositórios (Pastas) Principais

Para fins de estudo e organização, este mono-repositório simula os seguintes repositórios reais:

### 1. Camada de Produto e Workload
- **`web-frontend/`**: Aplicação de código-fonte Frontend (Vanilla JS).
- **`web-backend/`**: Aplicação de código-fonte Backend (FastAPI).
- **`acme-workload-events/`**: Repositório GitOps do time de produto. Contém os manifestos Kubernetes (Deployment, HPA) da aplicação. O ArgoCD monitora esta pasta.

### 2. Camada de Infraestrutura e Plataforma
- **`acme-iac-platform/`**: Repositório Terraform. Provisiona todos os serviços em nuvem (CosmosDB, Redis, RabbitMQ, Storage e Key Vault). Onde rodam as pipelines de `plan` e `apply`.
- **`acme-gitops-extensions/`**: Repositório de extensões do ArgoCD gerenciado por SRE. Contém os templates `ExternalSecret` separados por ambiente/região (ex: `envs/uat/us/templates/`).

### 3. Observabilidade
- **`observability/new-relic/`**: Monitoramento da aplicação (APM, logs da app).
- **`observability/azure-monitor/`**: Monitoramento da infraestrutura Cloud e dados.

### 4. Simulação Local
- **`local-env/`**: Contém o `docker-compose.yaml` com o emulador **floci-az**, permitindo que você rode e teste toda essa arquitetura (Terraform, Key Vault, Cosmos DB, etc.) na sua máquina **sem custo algum**. Leia o README dessa pasta para saber como conectá-lo.

---
**Dica Prática:** Explore as pastas `acme-workload-events/` e `acme-gitops-extensions/` para ver exemplos práticos de como o fluxo do External Secrets Operator (ESO) e do Deployment estão conectados!