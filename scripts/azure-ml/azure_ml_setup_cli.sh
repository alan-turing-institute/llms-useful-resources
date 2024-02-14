#! /usr/bin/env bash

# Arguments
SUBSCRIPTION_NAME=${1}

# Fixed values
LOCATION="eastus2"
RESOURCE_GROUP_NAME="rg-llm-endpoint"
WORKSPACE_NAME="llm-endpoint-ml"

# Ensure that the user is logged in
if ! (az account show > /dev/null); then
    az login
fi

echo "Setting up Azure ML workspace in '$SUBSCRIPTION_NAME'..."

# Switch subscription
echo "Setting account to '$SUBSCRIPTION_NAME'..."
az account set --subscription "$SUBSCRIPTION_NAME" --only-show-errors > /dev/null || exit 1

# Set up a resource group
echo "Creating resource group '$RESOURCE_GROUP_NAME'..."
az group create --location "$LOCATION" --name "$RESOURCE_GROUP_NAME" --only-show-errors > /dev/null || exit 2
echo "✅ Resource group '$RESOURCE_GROUP_NAME'"

# Set up Azure ML workspace
echo "Creating Azure ML workspace '$WORKSPACE_NAME'..."
az ml workspace create --name "$WORKSPACE_NAME" --resource-group "$RESOURCE_GROUP_NAME" --location "$LOCATION" --only-show-errors > /dev/null || exit 3
echo "✅ Azure ML workspace '$WORKSPACE_NAME'"
