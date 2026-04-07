#!/bin/bash

set -e

echo "🔄 Updating system..."
sudo apt update -y

echo "📦 Installing dependencies..."
sudo apt install -y curl apt-transport-https ca-certificates

# -----------------------------
# Install kubectl
# -----------------------------
echo "⬇️ Installing kubectl..."

KUBECTL_VERSION=$(curl -L -s https://dl.k8s.io/release/stable.txt)

curl -LO "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl"

chmod +x kubectl
sudo mv kubectl /usr/local/bin/

echo "✅ kubectl installed: $(kubectl version --client)"

# -----------------------------
# Install kind
# -----------------------------
echo "⬇️ Installing kind..."

curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64

chmod +x kind
sudo mv kind /usr/local/bin/kind

echo "✅ kind installed: $(kind --version)"

echo "🎉 Installation complete!"
