# DevOps Full Deploy Stack Project

This project simulates an enterprise cloud architecture with separation of duties between Platform, Operations/GitOps, and Product teams.

## Architecture Diagram

The main workflow for resource provisioning and secret management works as follows:

1. **Infrastructure Setup**: Bash scripts provision Azure resources (databases, Key Vaults) in local emulators (`floci-az` and Cosmos DB emulator).
2. **acme-external-secrets**: Hosts `ExternalSecret` templates. ArgoCD synchronizes these templates in the K8s cluster.
3. **ESO (External Secrets Operator)**: Reads the Key Vault using the instructions from the `ExternalSecret` and generates a native Secret in the cluster.
4. **Workload (Application)**: The application is deployed by ArgoCD and simply consumes the native Secret injected as environment variables.

## Main Repositories (Folders)

For study and organization purposes, this mono-repo simulates the following real repositories:

### 1. Product and Workload Layer
- **`web-frontend/`**: Frontend source code application (Vanilla JS).
- **`web-backend/`**: Backend source code application (FastAPI).
- **`acme-workload-events/`**: GitOps repository of the product team. Contains Kubernetes manifests (Deployment, HPA) for the application. ArgoCD monitors this folder.

### 2. Infrastructure and Platform Layer
- **`acme-external-secrets/`**: ArgoCD extensions repository managed by SRE. Contains `ExternalSecret` templates separated by environment/region (e.g.: `envs/uat/us/templates/`).

### 3. Observability
- **`observability/new-relic/`**: Application monitoring (APM, app logs).
- **`observability/azure-monitor/`**: Cloud infrastructure and data monitoring.

### 4. Local Simulation
- **`local-env/`**: Contains the `docker-compose.yaml` with the **floci-az** and **Azure Cosmos DB** emulators, allowing you to run and test this entire architecture on your machine **at no cost**. Read the README in this folder to learn how to connect to it.

---
**Practical Tip:** Explore the `acme-workload-events/` and `acme-external-secrets/` folders to see practical examples of how the External Secrets Operator (ESO) workflow and Deployment are connected!