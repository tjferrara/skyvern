#!/bin/bash

set -e

echo "Starting Skyvern UI on Railway..."

# Set default port if not provided by Railway
export PORT=${PORT:-8080}

# Set API endpoints to connect to the API service
export VITE_API_BASE_URL=${VITE_API_BASE_URL:-"https://skyvern-production-5271.up.railway.app/api/v1"}
export VITE_WSS_BASE_URL=${VITE_WSS_BASE_URL:-"wss://skyvern-production-5271.up.railway.app/api/v1"}

echo "UI Configuration:"
echo "PORT: $PORT"
echo "API_BASE_URL: $VITE_API_BASE_URL"
echo "WSS_BASE_URL: $VITE_WSS_BASE_URL"

# Ensure required directories exist
mkdir -p /app/.streamlit

# Create or update Streamlit configuration
cat > /app/.streamlit/config.toml << EOF
[server]
port = $PORT
address = "0.0.0.0"
headless = true
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
EOF

# Create secrets.toml for API connection
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "Creating Streamlit secrets configuration..."
    cat > .streamlit/secrets.toml << EOF
[skyvern]
configs = [
    {"env" = "railway", "host" = "$VITE_API_BASE_URL", "orgs" = []}
]
EOF
    echo "Streamlit secrets.toml created."
fi

# Start the Streamlit UI
echo "Starting Skyvern Streamlit UI on port $PORT..."
exec streamlit run skyvern/forge/app.py --server.port=$PORT --server.address=0.0.0.0 