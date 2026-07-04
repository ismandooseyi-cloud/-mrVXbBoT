"""
Configuration settings for mrVXbBoT
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

class Config:
    """Bot configuration class"""
    
    # Bot token from environment variable
    BOT_TOKEN = os.getenv('BOT_TOKEN') or os.getenv('TELEGRAM_BOT_TOKEN')
    
    # API endpoints
    QR_API_URL = "https://api.qrserver.com/v1/create-qr-code/"
    IMAGE_GEN_API = "https://image.pollinations.ai/prompt/"
    
    # Supported image formats for conversion
    SUPPORTED_FORMATS = ['PNG', 'JPEG', 'WEBP', 'BMP', 'GIF']
    
    # Image compression quality (1-100)
    COMPRESSION_QUALITY = 50
    
    # Maximum file size (in bytes) - 20MB
    MAX_FILE_SIZE = 20 * 1024 * 1024
    
    # Logging configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required but not set in environment variables")
        return True
