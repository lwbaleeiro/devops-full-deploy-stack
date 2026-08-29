# Ambiente Local (Emulação Azure)

Este diretório contém os arquivos necessários para simular a nuvem Microsoft Azure localmente de forma 100% gratuita utilizando o **floci-az**.

## O que é o floci-az?

O [floci-az](https://floci.io/) é um emulador de código aberto super leve. Ele sobe um servidor local (geralmente na porta `4577`) que simula dezenas de APIs do Azure, como Cosmos DB, Blob Storage, Key Vault, Service Bus, entre outros.

Isso significa que você pode apontar o Terraform e o backend da aplicação para o `localhost:4577` e tudo funcionará como se você estivesse usando a nuvem real.

A interface web do floci está disponível em `http://localhost:4500`

## Como usar

Para facilitar a configuração do ambiente e a configuração dos certificados TLS (necessários pelo Terraform), criamos um script automatizado.

Certifique-se de ter o Docker e o Docker Compose instalados na sua máquina, então execute:

```bash
./start.sh
```

Este script irá:
1. Subir os containers do docker-compose.
2. Aguardar o floci-az inicializar.
3. Extrair o certificado autoassinado (TLS) do emulador e salvar localmente como `floci-cert.pem`.

No final da execução, ele indicará como exportar o certificado e as variáveis do `.env` na sua sessão para o uso do Terraform.

### Configurando o Terraform (acme-iac-platform)
No seu Terraform, você configura os endpoints customizados do AzureRM Provider para apontar para o `floci-az`:

```hcl
provider "azurerm" {
  features {}
  # Aponta a API do Azure para o floci-az
  environment = "public"
  custom_provider_endpoints {
    resource_manager_endpoint = "http://localhost:4577"
    active_directory_endpoint = "http://localhost:4577"
  }
}
```

### Configurando o Backend e o GitOps
No seu cluster local (Minikube), as variáveis de ambiente e o External Secrets Operator também devem apontar para a URL do floci-az para resgatar os secrets simulados do Key Vault.
