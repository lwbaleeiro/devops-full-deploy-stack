# Local Environment (Azure Emulation)

This directory contains the files needed to simulate the Microsoft Azure cloud locally, 100% free of charge, using **floci-az**.

## What is floci-az?

[floci-az](https://floci.io/) is an ultra-lightweight open-source emulator. It spins up a local server (usually on port `4577`) that simulates dozens of Azure APIs, such as Cosmos DB, Blob Storage, Key Vault, Service Bus, among others.

This means you can point your Terraform and the application backend to `localhost:4577` and everything will work as if you were using the real cloud.

The floci web interface is available at `http://localhost:4500`

## How to use

To simplify the environment setup and the configuration of TLS certificates (required by Terraform), we created an automated script.

Ensure you have Docker and Docker Compose installed on your machine, then run:

```bash
./start.sh
```

This script will:
1. Spin up the docker-compose containers.
2. Wait for floci-az to initialize.
3. Extract the self-signed certificate (TLS) from the emulator and save it locally as `floci-cert.pem`.

At the end of the execution, it will show you how to export the certificate and the `.env` variables in your session for Terraform to use.

### Configuring Terraform (acme-iac-platform)
In your Terraform configuration, you set up the custom endpoints for the AzureRM Provider to point to `floci-az`:

```hcl
provider "azurerm" {
  features {}
  # Points the Azure API to floci-az
  environment = "public"
  custom_provider_endpoints {
    resource_manager_endpoint = "http://localhost:4577"
    active_directory_endpoint = "http://localhost:4577"
  }
}
```

### Configuring the Backend and GitOps
In your local cluster (Minikube), environment variables and the External Secrets Operator must also point to the floci-az URL to fetch the simulated secrets from the Key Vault.
