#!/bin/bash

set -e

echo "Starting Skyvern on Railway..."

# Debug: Check Python path and module structure
echo "=== Python Path Debug ==="
echo "PYTHONPATH: $PYTHONPATH"
echo "Current directory: $(pwd)"
echo "Python sys.path:"
python -c "import sys; print('\n'.join(sys.path))"
echo "=== Client Module Structure ==="
find /app/skyvern/client -name "*.py" | head -10
echo "=== Testing imports ==="
python -c "
try:
    import skyvern.client.artifacts
    print('✓ skyvern.client.artifacts import successful')
except Exception as e:
    print(f'✗ skyvern.client.artifacts import failed: {e}')

try:
    from skyvern.client.artifacts.client import ArtifactsClient
    print('✓ ArtifactsClient import successful')
except Exception as e:
    print(f'✗ ArtifactsClient import failed: {e}')
"

# Set default port if not provided by Railway
export PORT=${PORT:-8000}

# Railway provides DATABASE_URL, but Skyvern expects DATABASE_STRING
if [ -n "$DATABASE_URL" ]; then
    export DATABASE_STRING="$DATABASE_URL"
fi

# Set default browser type for Railway (headless for better performance)
export BROWSER_TYPE=${BROWSER_TYPE:-chromium-headless}

# Ensure required directories exist
mkdir -p "$VIDEO_PATH" "$HAR_PATH" "$LOG_PATH" "$ARTIFACT_STORAGE_PATH" /app/.streamlit

# Run database migrations
echo "Running database migrations..."
alembic upgrade head
alembic check

# Create organization and API token if secrets.toml doesn't exist
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "Creating organization and API token..."
    org_output=$(python scripts/create_organization.py Skyvern-Open-Source)
    api_token=$(echo "$org_output" | awk '/token=/{gsub(/.*token='\''|'\''.*/, ""); print}')
    
    # Get Railway's provided URL or use localhost
    RAILWAY_URL=${RAILWAY_STATIC_URL:-"http://localhost:$PORT"}
    
    # Update the secrets file with Railway URL
    echo -e "[skyvern]\nconfigs = [\n    {\"env\" = \"railway\", \"host\" = \"$RAILWAY_URL/api/v1\", \"orgs\" = [{name=\"Skyvern\", cred=\"$api_token\"}]}\n]" > .streamlit/secrets.toml
    echo ".streamlit/secrets.toml file updated with organization details."
fi

# Setup virtual display for headless browser operations
echo "Setting up virtual display..."
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x16 -ac -nolisten tcp &
XVFB_PID=$!

# Function to cleanup on exit
cleanup() {
    echo "Cleaning up..."
    kill $XVFB_PID 2>/dev/null || true
    exit 0
}

# Setup trap to catch signals
trap cleanup SIGTERM SIGINT

# Start the streaming service in background
echo "Starting streaming service..."
python run_streaming.py > /dev/null 2>&1 &
STREAMING_PID=$!

# Start the main Skyvern application
echo "Starting Skyvern application on port $PORT..."
exec python -m skyvern.forge 