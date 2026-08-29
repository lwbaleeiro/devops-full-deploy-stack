# Workload: Events App

This repository is managed by product teams and contains the Kubernetes manifests for the events frontend and backend.

## Structure

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

## Usage

The manifests are automatically synchronized by ArgoCD in the respective environments and regions.