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
echo "=== Database Configuration Debug ==="
echo "DATABASE_URL: ${DATABASE_URL:-'NOT SET'}"
echo "DATABASE_STRING: ${DATABASE_STRING:-'NOT SET'}"

if [ -n "$DATABASE_URL" ]; then
    # Convert postgresql:// to postgresql+psycopg:// for SQLAlchemy to use psycopg3
    export DATABASE_STRING="${DATABASE_URL/postgresql:\/\//postgresql+psycopg:\/\/}"
    echo "✓ DATABASE_STRING set from DATABASE_URL (converted to use psycopg driver)"
else
    echo "✗ DATABASE_URL not provided by Railway"
fi

echo "Final DATABASE_STRING: ${DATABASE_STRING:-'NOT SET'}"

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
    
    # Export the API token for the frontend to use
    export VITE_SKYVERN_API_KEY="$api_token"
    echo "✓ API token exported for frontend: ${api_token:0:20}..."
    
    # Save the API token to a file that can be read by other processes
    echo "$api_token" > /tmp/skyvern_api_key.txt
    echo "✓ API token saved to /tmp/skyvern_api_key.txt"
else
    echo "Organization already exists, extracting API token..."
    # Extract API token from existing secrets.toml
    api_token=$(grep -o 'cred="[^"]*"' .streamlit/secrets.toml | sed 's/cred="//;s/"//')
    if [ -n "$api_token" ]; then
        export VITE_SKYVERN_API_KEY="$api_token"
        echo "$api_token" > /tmp/skyvern_api_key.txt
        echo "✓ Existing API token found and exported: ${api_token:0:20}..."
    else
        echo "✗ Could not extract API token from secrets.toml"
    fi
fi

# Setup virtual display for headless browser operations
echo "Setting up virtual display..."
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x16 -ac -nolisten tcp &
XVFB_PID=$!

# Setup trap to catch signals (cleanup function defined below)
trap cleanup SIGTERM SIGINT

# Start the streaming service in background
echo "Starting streaming service..."
python run_streaming.py > /dev/null 2>&1 &
STREAMING_PID=$!

# Update cleanup function
cleanup() {
    echo "Cleaning up..."
    kill $XVFB_PID 2>/dev/null || true
    kill $STREAMING_PID 2>/dev/null || true
    exit 0
}

# Start the main Skyvern service (API + Frontend)
echo "Starting Skyvern service (API + Frontend) on port $PORT..."
exec python -m skyvern.forge.__main___railway 