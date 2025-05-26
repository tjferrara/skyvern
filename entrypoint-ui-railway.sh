#!/bin/bash

set -e

echo "Starting Skyvern React UI on Railway..."

# Set default port if not provided by Railway
export PORT=${PORT:-8080}

# Set API endpoints to connect to the API service
export VITE_API_BASE_URL=${VITE_API_BASE_URL:-"https://skyvern-production-5271.up.railway.app/api/v1"}
export VITE_WSS_BASE_URL=${VITE_WSS_BASE_URL:-"wss://skyvern-production-5271.up.railway.app/api/v1"}

echo "UI Configuration:"
echo "PORT: $PORT"
echo "API_BASE_URL: $VITE_API_BASE_URL"
echo "WSS_BASE_URL: $VITE_WSS_BASE_URL"

# Start the React frontend using serve
echo "Starting Skyvern React UI on port $PORT..."
exec serve -s /app/dist -l $PORT 