"""
Utility functions for mrVXbBoT
"""

import io
import logging
import requests
from PIL import Image
from urllib.parse import urlparse
import pyshorteners
from config import Config

logger = logging.getLogger(__name__)

class ImageUtils:
    """Image processing utilities"""
    
    @staticmethod
    def convert_image(image_data: bytes, target_format: str) -> io.BytesIO:
        """
        Convert image to different format
        
        Args:
            image_data: Raw image data
            target_format: Target format (PNG, JPEG, WEBP, BMP, GIF)
        
        Returns:
            BytesIO object with converted image
        """
        try:
            img = Image.open(io.BytesIO(image_data))
            
            # Handle alpha channel for JPEG
            if target_format.upper() == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                img = background
            
            output = io.BytesIO()
            img.save(output, format=target_format.upper(), quality=95, optimize=True)
            output.seek(0)
            return output
            
        except Exception as e:
            logger.error(f"Image conversion error: {e}")
            raise Exception(f"Failed to convert image: {str(e)}")
    
    @staticmethod
    def compress_image(image_data: bytes, quality: int = Config.COMPRESSION_QUALITY) -> io.BytesIO:
        """
        Compress image by reducing quality
        
        Args:
            image_data: Raw image data
            quality: Compression quality (1-100)
        
        Returns:
            BytesIO object with compressed image
        """
        try:
            img = Image.open(io.BytesIO(image_data))
            output = io.BytesIO()
            
            # Use original format or fallback to JPEG
            img_format = img.format or 'JPEG'
            
            # For PNG, use optimize flag instead of quality
            if img_format.upper() == 'PNG':
                img.save(output, format='PNG', optimize=True)
            else:
                img.save(output, format='JPEG', quality=quality, optimize=True)
            
            output.seek(0)
            return output
            
        except Exception as e:
            logger.error(f"Compression error: {e}")
            raise Exception(f"Failed to compress image: {str(e)}")
    
    @staticmethod
    def get_image_info(image_data: bytes) -> dict:
        """
        Get image information
        
        Returns:
            Dictionary with image info
        """
        try:
            img = Image.open(io.BytesIO(image_data))
            return {
                'format': img.format or 'Unknown',
                'mode': img.mode,
                'width': img.width,
                'height': img.height,
                'size_kb': len(image_data) / 1024,
                'channels': len(img.getbands())
            }
        except Exception as e:
            logger.error(f"Info extraction error: {e}")
            raise Exception(f"Failed to get image info: {str(e)}")

class URLUtils:
    """URL processing utilities"""
    
    @staticmethod
    def shorten_url(url: str) -> str:
        """
        Shorten URL using TinyURL
        
        Args:
            url: Long URL to shorten
        
        Returns:
            Shortened URL
        """
        try:
            # Validate URL
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Use pyshorteners with TinyURL
            shortener = pyshorteners.Shortener()
            short_url = shortener.tinyurl.short(url)
            return short_url
            
        except Exception as e:
            logger.error(f"URL shortening error: {e}")
            raise Exception(f"Failed to shorten URL: {str(e)}")
    
    @staticmethod
    def generate_qr(text: str) -> io.BytesIO:
        """
        Generate QR code from text or URL
        
        Args:
            text: Text or URL to encode
        
        Returns:
            BytesIO object with QR code image
        """
        try:
            # API call to qrserver.com
            response = requests.get(
                f"{Config.QR_API_URL}",
                params={
                    'size': '400x400',
                    'data': text,
                    'margin': '10',
                    'bgcolor': 'ffffff',
                    'color': '000000'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return io.BytesIO(response.content)
            else:
                raise Exception(f"API returned status code: {response.status_code}")
                
        except Exception as e:
            logger.error(f"QR generation error: {e}")
            raise Exception(f"Failed to generate QR code: {str(e)}")

class ImageGenerator:
    """AI Image generation utilities"""
    
    @staticmethod
    def generate_image(prompt: str) -> io.BytesIO:
        """
        Generate image from text prompt using free API
        
        Args:
            prompt: Text description
        
        Returns:
            BytesIO object with generated image
        """
        try:
            # Use Pollinations.ai API
            response = requests.get(
                f"{Config.IMAGE_GEN_API}{prompt}",
                params={
                    'width': '512',
                    'height': '512',
                    'nologo': 'true'
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return io.BytesIO(response.content)
            else:
                raise Exception(f"API returned status code: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Image generation error: {e}")
            raise Exception(f"Failed to generate image: {str(e)}")

def is_valid_url(url: str) -> bool:
    """Check if URL is valid"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def format_file_size(size_bytes: float) -> str:
    """Format file size in human-readable format"""
    if size_bytes < 1024:
        return f"{size_bytes:.1f} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
