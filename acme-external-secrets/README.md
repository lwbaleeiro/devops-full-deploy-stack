# acme-external-secrets

This repository contains GitOps templates (ExternalSecrets) managed by Operations/SRE.

## Folder Structure

Files are organized by environment (`envs`) and region (`us`/`br`):

```
envs/
├── uat/
│   ├── br/
│   └── us/
└── prod/
    ├── br/
    └── us/
```

## Usage Example

To create an ExternalSecret in the `uat` environment in the `us` region:

1. Create a folder: `mkdir -p envs/uat/us`
2. Add the ExternalSecret YAML file inside the folder.
3. ArgoCD will synchronize automatically.
