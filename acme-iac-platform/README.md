# Provisionamento (IaC) - Platform

Este repositório contém templates Terraform para provisionamento de recursos Azure (Bancos, Cache, Storage, RabbitMQ e Key Vault).

## Estrutura de Pastas

```
.tf/
├── shared/                # Recursos compartilhados (ex: Resource Groups)
├── uat/                   # Ambiente UAT
│   ├── br/                # Região Brasil
│   └── us/                # Região US
├── prod/                  # Ambiente de Produção
│   ├── br/                # Região Brasil
│   └── us/                # Região US
├── modules/               # Módulos Terraform reutilizáveis
└── templates/             # Templates para geração de arquivos
```

## Uso

As pipelines Azure DevOps executam o `terraform plan` e `terraform apply` para provisionar os recursos nos respectivos ambientes e regiões.
