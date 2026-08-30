#!/bin/bash

# Configuration
FLOCI_URL="http://localhost:4577"
SUBSCRIPTION_ID="00000000-0000-0000-0000-000000000000"
TENANT_ID="00000000-0000-0000-0000-000000000000"
RESOURCE_GROUP="rg-acme-events-uat"
KEY_VAULT_NAME="kv-uat-us-001"
LOCATION="eastus"

echo "Creating Resource Group: $RESOURCE_GROUP..."
curl -s -X PUT -H "Content-Type: application/json" \
  -d "{\"location\":\"$LOCATION\"}" \
  "$FLOCI_URL/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP?api-version=2021-04-01"

echo ""
echo "Creating Key Vault: $KEY_VAULT_NAME..."
curl -s -X PUT -H "Content-Type: application/json" \
  -d "{\"location\":\"$LOCATION\",\"properties\":{\"sku\":{\"family\":\"A\",\"name\":\"standard\"},\"tenantId\":\"$TENANT_ID\"}}" \
  "$FLOCI_URL/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.KeyVault/vaults/$KEY_VAULT_NAME?api-version=2021-10-01"

echo ""
echo "Creating Mock Secret for Cosmos DB in Key Vault..."
# Using the well-known Cosmos DB emulator default key and endpoint
COSMOS_CONN_STRING="AccountEndpoint=https://localhost:8081/;AccountKey=C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==;"

curl -s -X PUT -H "Content-Type: application/json" \
  -d "{\"properties\":{\"value\":\"$COSMOS_CONN_STRING\"}}" \
  "$FLOCI_URL/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.KeyVault/vaults/$KEY_VAULT_NAME/secrets/cosmos-connection-string?api-version=2021-10-01"

echo ""
echo "Setup complete!"
