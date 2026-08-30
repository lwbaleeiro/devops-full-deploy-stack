# Acme Local Infrastructure (Azure Emulation)

This directory contains the files needed to simulate the Microsoft Azure cloud locally, 100% free of charge, using **floci-az** and the **Azure Cosmos DB Emulator**.

## Architecture

We use a combination of Docker containers to mimic the required Azure services locally:

1. **floci-az** (`localhost:4577`): An ultra-lightweight emulator that simulates Azure APIs. We use it to mock our Resource Groups, Key Vaults, and Storage Accounts.
2. **Azure Cosmos DB Emulator** (`localhost:8081`): The official Microsoft emulator used to provide full Cosmos DB NoSQL capabilities.

### UIs and Dashboards
- The **floci-az web interface** is available at `http://localhost:4500`
- The **Azure Cosmos DB Explorer** is available at `https://localhost:8081/_explorer/index.html` *(Accept the self-signed certificate warning to access)*

## Setup Instructions

To simplify the environment setup, we replaced Terraform with automated bash scripts that directly provision the mock infrastructure via API.

### 1. Start the Emulators

Ensure you have Docker and Docker Compose installed on your machine, then run:

```bash
./start.sh
```

This script will:
1. Spin up the docker-compose containers (`floci-az`, `floci-ui`, and `cosmos-emulator`).
2. Wait for `floci-az` to initialize.
3. Extract the self-signed certificate (TLS) from the emulator and save it locally as `floci-cert.pem`. *(This certificate is required by local Kubernetes clients or applications like the External Secrets Operator to trust the HTTPS endpoint of the emulator).*

### 2. Provision Resources

Once the emulators are running, you need to create the Azure resources (Resource Group, Key Vault, Secrets, and Storage). Run the setup script:

```bash
./setup-infrastructure.sh
```

This script provisions the resources in `floci-az` and injects the Cosmos DB connection string directly into the local Key Vault as a secret (`cosmos-connection-string`), seamlessly bridging the two emulators.

## Configuring the Backend and GitOps

In your local cluster (e.g., Minikube), the External Secrets Operator (ESO) must point to the `floci-az` URL to fetch the simulated secrets from the `devstoreaccount1` Key Vault. Be sure to mount or inject the `floci-cert.pem` so the ESO trusts the local TLS certificate.
