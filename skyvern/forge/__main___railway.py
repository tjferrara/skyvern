import uvicorn
from skyvern.config import settings
from skyvern.forge.api_app_railway import get_agent_app

if __name__ == "__main__":
    app = get_agent_app()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.PORT,
        log_level="info",
    ) 