import os
from dotenv import load_dotenv


class AppConfig:
    """Class to manage all configuration settings for the application"""

    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Load feature flags
        self.ENVIRONMENT = os.environ.get("ENVIRONMENT", "development").lower()
        self.PORT = os.environ.get("PORT", 8000)
        self.OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
        self.MOCK_TEST = os.getenv("MOCK_TEST", "False").lower() in ("true", "1", "yes")

# Create a singleton instance
app_config = AppConfig()
