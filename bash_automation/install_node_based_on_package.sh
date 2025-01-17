#!/bin/bash

# Script: install_node_based_on_package.sh
# Purpose: Reads node version from package.json and installs/uses the correct version with nvm.
# If node engine is not specified, checks Angular version for compatibility.

# Exit immediately if a command exits with a non-zero status
set -e

# Function to extract a JSON key value
extract_value() {
    local key=$1
    jq -r ".$key // empty" package.json
}

# Function to determine compatible Node.js version for Angular
get_node_version_for_angular() {
    local angular_version=$1

    # Compatibility matrix for Angular and Node.js versions
    if [[ "$angular_version" =~ ^15 ]]; then
        echo "16"
    elif [[ "$angular_version" =~ ^14 ]]; then
        echo "14"
    elif [[ "$angular_version" =~ ^13 ]]; then
        echo "14"
    elif [[ "$angular_version" =~ ^12 ]]; then
        echo "14"
    else
        echo "16" # Default to LTS version
    fi
}

# Ensure package.json exists
if [[ ! -f package.json ]]; then
    echo "Error: package.json not found in the current directory."
    exit 1
fi

# Extract Node.js version from package.json under "engines"
node_version=$(extract_value "engines.node")

# If Node.js version is found
if [[ -n "$node_version" ]]; then
    echo "Node.js version specified in package.json: $node_version"
    nvm install "$node_version"
    nvm use "$node_version"
else
    # If Node.js version is not specified, check for Angular version
    echo "Node.js version not specified in package.json. Checking Angular version..."
    angular_version=$(jq -r '.dependencies["@angular/core"] // empty' package.json)

    if [[ -n "$angular_version" ]]; then
        echo "Angular version specified in package.json: $angular_version"
        compatible_node_version=$(get_node_version_for_angular "$angular_version")
        echo "Installing compatible Node.js version for Angular $angular_version: $compatible_node_version"
        nvm install "$compatible_node_version"
        nvm use "$compatible_node_version"
    else
        echo "Neither Node.js version nor Angular version specified in package.json."
        echo "Installing latest Node.js LTS version as default."
        nvm install --lts
        nvm use --lts
    fi
fi

echo "Node.js setup completed successfully."
