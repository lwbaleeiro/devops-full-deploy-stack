# Provisioning (IaC) - Platform

This repository contains Terraform templates for provisioning Azure resources (Databases, Cache, Storage, RabbitMQ, and Key Vault).

## Folder Structure

```
.tf/
├── shared/                # Shared resources (e.g. Resource Groups)
├── uat/                   # UAT Environment
│   ├── br/                # Brazil Region
│   └── us/                # US Region
├── prod/                  # Production Environment
│   ├── br/                # Brazil Region
│   └── us/                # US Region
├── modules/               # Reusable Terraform modules
└── templates/             # Templates for file generation
```

## Usage

Azure DevOps pipelines execute `terraform plan` and `terraform apply` to provision the resources in the respective environments and regions.
