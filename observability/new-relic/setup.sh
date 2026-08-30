#!/bin/bash

echo "============================================="
echo "Installing New Relic on Local Kubernetes Cluster"
echo "============================================="

# Ensure helm is installed
if ! command -v helm &> /dev/null
then
    echo "Helm could not be found. Please install helm first (https://helm.sh/docs/intro/install/)"
    exit 1
fi

echo "Adding New Relic Helm repository..."
helm repo add newrelic https://helm-charts.newrelic.com
helm repo update

# Ask for License Key or use environment variable
if [ -z "$NEW_RELIC_LICENSE_KEY" ]; then
    read -p "Enter your New Relic License Key (or press enter to use a dummy key): " NEW_RELIC_LICENSE_KEY
fi

if [ -z "$NEW_RELIC_LICENSE_KEY" ]; then
    echo "No license key provided. Using a dummy key. Data will NOT be sent to New Relic."
    NEW_RELIC_LICENSE_KEY="dummy-license-key-for-local-testing"
fi

CLUSTER_NAME="local-dev-cluster"

echo "Installing nri-bundle via Helm..."
helm upgrade --install newrelic-bundle newrelic/nri-bundle \
  --set global.licenseKey=$NEW_RELIC_LICENSE_KEY \
  --set global.cluster=$CLUSTER_NAME \
  --namespace newrelic --create-namespace \
  --set newrelic-infrastructure.privileged=true \
  --set ksm.enabled=true \
  --set prometheus.enabled=true \
  --set kubeEvents.enabled=true \
  --set logging.enabled=true

echo ""
echo "============================================="
echo "New Relic setup complete!"
echo "Check the pods status with: kubectl get pods -n newrelic"
echo "============================================="
