#!/bin/bash

# This script starts up the local environment (floci-az) and prepares the certificates for use with Terraform

set -e

echo "Starting up local environment..."
docker compose -f docker-compose.yaml up -d

echo "Waiting for floci-az to start to extract the TLS certificate..."

# Wait until the endpoint responds (attempts for 15 seconds)
max_retries=15
counter=0
until curl -s http://localhost:4577/_floci/tls-cert > /dev/null; do
    sleep 1
    counter=$((counter+1))
    if [ $counter -ge $max_retries ]; then
        echo "Timeout waiting for floci-az to start"
        exit 1
    fi
done

echo "floci-az started successfully"

echo "Downloading self-signed TLS certificate..."
curl -s http://localhost:4577/_floci/tls-cert > floci-cert.pem

echo "Certificate saved to 'local-env/floci-cert.pem'"
echo ""
echo "--------------------------------------------------------"
echo "All set! The local emulators (floci-az and Cosmos DB) are running."
echo ""
echo "To provision the local Azure resources, run the setup script:"
echo ""
echo "  ./setup-infrastructure.sh"
echo "--------------------------------------------------------"
