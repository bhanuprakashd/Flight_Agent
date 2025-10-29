"""Configuration file for Flight Agent"""
import os

class config:
    """Configuration settings for Flight Agent"""
    # Google Cloud settings
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    # Model settings
    MODEL_NAME = "gemini/gemini-2.5-flash"
    TEMPERATURE = 0.1
    
    # MCP settings
    MCP_TIMEOUT = 360  # 6 minutes timeout for MCP calls
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # App settings
    APP_NAME = "flight_agent_app"
