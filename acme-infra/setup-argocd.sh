#!/bin/bash

# Configuration
ARGOCD_NAMESPACE="argocd"
REPO_URL="https://github.com/lwbaleeiro/devops-full-deploy-stack.git"

echo "============================================="
echo "Installing ArgoCD on Local Kubernetes Cluster"
echo "============================================="

# Create namespace
echo "[1/4] Creating namespace '$ARGOCD_NAMESPACE'..."
kubectl create namespace $ARGOCD_NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Install ArgoCD
echo "[2/4] Applying ArgoCD stable manifests..."
kubectl apply -n $ARGOCD_NAMESPACE -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for components to be ready
echo "[3/4] Waiting for ArgoCD server to be ready (this may take a minute)..."
kubectl wait --for=condition=available deployment/argocd-server -n $ARGOCD_NAMESPACE --timeout=300s

echo "[4/4] Deploying Root Application..."
cat <<EOF | kubectl apply -f -
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: $REPO_URL
    targetRevision: HEAD
    path: acme-workload-events # Starts deploying the backend workload as an example
  destination:
    server: https://kubernetes.default.svc
    namespace: events-app
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
EOF

echo ""
echo "============================================="
echo "ArgoCD setup complete!"
echo "============================================="
echo "To access the ArgoCD UI, run in a new terminal:"
echo "  kubectl port-forward svc/argocd-server -n argocd 8080:443"
echo ""
echo "Open your browser at: https://localhost:8080"
echo "Default username: admin"
echo "To get the password, run:"
echo "  kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath=\"{.data.password}\" | base64 -d; echo"
echo "============================================="
