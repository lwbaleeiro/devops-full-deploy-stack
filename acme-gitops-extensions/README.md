# GitOps Extensions

Este repositório contém templates GitOps (ExternalSecrets) gerenciados por Operações/SRE.

## Estrutura de Pastas

Os arquivos estão organizados por ambiente (`envs`) e região (`us`/`br`):

```
envs/
├── uat/
│   ├── br/
│   └── us/
└── prod/
    ├── br/
    └── us/
```

## Exemplo de Uso

Para criar um ExternalSecret no ambiente `uat` na região `us`:

1. Crie uma pasta: `mkdir -p envs/uat/us`
2. Adicione o arquivo YAML do ExternalSecret dentro da pasta.
3. O ArgoCD sincronizará automaticamente.
