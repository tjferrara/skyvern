# Skyvern Railway Deployment Guide

This guide will help you deploy Skyvern on Railway with the optimized configuration.

## Prerequisites

1. A Railway account (sign up at [railway.app](https://railway.app))
2. A PostgreSQL database (Railway provides this)
3. API keys for your preferred LLM provider (OpenAI, Anthropic, etc.)

## Quick Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/skyvern)

## Manual Deployment Steps

### 1. Create a New Railway Project

1. Go to [railway.app](https://railway.app) and create a new project
2. Choose "Deploy from GitHub repo" and select your Skyvern repository
3. Railway will automatically detect the `railway.toml` configuration

### 2. Add a PostgreSQL Database

1. In your Railway project dashboard, click "New Service"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically create a PostgreSQL instance and set the `DATABASE_URL` environment variable

### 3. Configure Environment Variables

Add the following environment variables in your Railway project settings:

#### Required Variables
```bash
# Database (automatically set by Railway PostgreSQL service)
DATABASE_URL=postgresql://username:password@host:port/database

# LLM Provider (choose one or more)
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GEMINI_API_KEY=your_gemini_api_key

# LLM Configuration
ENABLE_OPENAI=true
LLM_KEY=OPENAI_GPT4O
# OR for Anthropic
# ENABLE_ANTHROPIC=true
# LLM_KEY=ANTHROPIC_CLAUDE3.5_SONNET
```

#### Optional Variables
```bash
# Browser Configuration
BROWSER_TYPE=chromium-headless
ENABLE_CODE_BLOCK=true

# Bitwarden Integration (optional)
BITWARDEN_CLIENT_ID=your_bitwarden_client_id
BITWARDEN_CLIENT_SECRET=your_bitwarden_client_secret
BITWARDEN_MASTER_PASSWORD=your_bitwarden_master_password

# AWS Integration (optional)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-west-2
```

### 4. Deploy

1. Push your code to GitHub (if not already done)
2. Railway will automatically build and deploy using the `Dockerfile.railway`
3. The deployment process will:
   - Build the Docker image with optimized dependencies
   - Run database migrations
   - Start the Skyvern application
   - Set up the virtual display for browser automation

### 5. Access Your Application

Once deployed, Railway will provide you with a public URL. You can access:
- **API**: `https://your-app.railway.app/api/v1`
- **Health Check**: `https://your-app.railway.app/api/v1/health`

## Key Optimizations for Railway

### 1. Fixed Circular Import Issue
- Properly initialized the `artifacts` module in `skyvern/client/artifacts/__init__.py`
- This resolves the import error that was causing deployment failures

### 2. Railway-Specific Dockerfile
- Uses multi-stage build for smaller image size
- Optimized for Railway's ephemeral filesystem
- Uses `/tmp` directories for temporary files
- Includes all necessary system dependencies for browser automation

### 3. Environment Variable Handling
- Automatically converts Railway's `DATABASE_URL` to Skyvern's expected `DATABASE_STRING`
- Uses Railway's provided `PORT` environment variable
- Configures headless browser mode for better performance

### 4. Resource Optimization
- Uses `chromium-headless` browser type for lower memory usage
- Optimized virtual display setup
- Proper cleanup on container shutdown

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Ensure the PostgreSQL service is running in Railway
   - Check that `DATABASE_URL` is properly set

2. **Browser Automation Issues**
   - The deployment uses headless Chrome which should work in Railway's environment
   - If you encounter issues, check the logs for Xvfb startup messages

3. **Memory Issues**
   - Railway's free tier has memory limits
   - Consider upgrading to a paid plan for production workloads
   - Monitor memory usage in Railway's metrics dashboard

4. **Build Timeouts**
   - The initial build may take 10-15 minutes due to Playwright browser installation
   - Subsequent builds will be faster due to Docker layer caching

### Viewing Logs

Access logs through Railway's dashboard:
1. Go to your project in Railway
2. Click on your service
3. Navigate to the "Logs" tab

### Health Checks

The application includes a health check endpoint at `/api/v1/health` that Railway uses to monitor the service status.

## Scaling Considerations

For production deployments:

1. **Database**: Use Railway's PostgreSQL with appropriate resources
2. **Memory**: Ensure adequate memory allocation for browser automation
3. **Storage**: Use external storage (S3) for artifacts and videos
4. **Monitoring**: Set up proper logging and monitoring

## Security Notes

1. Never commit API keys to your repository
2. Use Railway's environment variables for all sensitive data
3. Consider using Railway's private networking for database connections
4. Regularly rotate API keys and credentials

## Support

If you encounter issues:
1. Check the Railway deployment logs
2. Review the Skyvern documentation
3. Open an issue on the Skyvern GitHub repository 