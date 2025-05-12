import uvicorn
from app.configs.app_config import app_config


if __name__ == "__main__":
    print(f"Starting uvicorn server in {app_config.ENVIRONMENT} environment on port {app_config.PORT}")
    print(f"MOCK_TEST: {app_config.MOCK_TEST}")

    # Start the Uvicorn server
    uvicorn.run(
        "app.main:app",  # Make sure this matches your actual module path
        host="0.0.0.0",
        port=8000,
        reload=(app_config.ENVIRONMENT != "production")  # Auto-reload in development mode
    )