# Workload: Events App

Este repositório é gerenciado por equipes de produto e contém os manifestos Kubernetes para o frontend e backend de eventos.

## Estrutura

```
.k8s/
├── helm/
├── overlays/
│   ├── uat/
│   │   ├── br/
│   │   └── us/
│   └── prod/
│       ├── br/
│       └── us/
└── templates/
```

## Uso

Os manifestos são sincronizados automaticamente pelo ArgoCD nos respectivos ambientes e regiões.
    