terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}

  skip_provider_registration = true

  subscription_id = "00000000-0000-0000-0000-000000000000"
  tenant_id       = "00000000-0000-0000-0000-000000000000"
  client_id       = "00000000-0000-0000-0000-000000000000"
  client_secret   = "dummy-secret"

  use_cli  = false
  use_oidc = false
  use_msi  = false

  metadata_host = "localhost:4577"
}

# 1. Grupo de Recursos
resource "azurerm_resource_group" "rg" {
  name     = "rg-acme-events-uat"
  location = "eastus"
}

# 2. Key Vault (onde os segredos serão guardados para o External Secrets ler depois)
resource "azurerm_key_vault" "kv" {
  name                     = "kv-uat-us-001"
  location                 = azurerm_resource_group.rg.location
  resource_group_name      = azurerm_resource_group.rg.name
  tenant_id                = "00000000-0000-0000-0000-000000000000"
  sku_name                 = "standard"
  purge_protection_enabled = false
}

# 3. Cosmos DB (Simulando nosso banco de dados)
resource "azurerm_cosmosdb_account" "db" {
  name                = "cosmos-events-uat"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = azurerm_resource_group.rg.location
    failover_priority = 0
  }
}

# 4. Criando um Secret de mentirinha no Key Vault com a connection string do Cosmos
resource "azurerm_key_vault_secret" "cosmos_secret" {
  name = "cosmos-connection-string"
  # O floci simula a criação de chaves. Aqui estamos injetando uma URL fake
  value        = "AccountEndpoint=http://localhost:4577;AccountKey=fake_key;"
  key_vault_id = azurerm_key_vault.kv.id
}
