"""
mrVXbBoT - All-in-One Telegram Utility Bot
Deployed on Railway with GitHub integration
"""

import os
import logging
import sys
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from config import Config
from handlers import (
    start_command, help_command, shorten_command, 
    qr_command, generate_command, handle_image,
    handle_text, handle_callback, error_handler
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main function to start the bot"""
    try:
        # Get bot token from config
        token = Config.BOT_TOKEN
        
        if not token:
            logger.error("❌ BOT_TOKEN not found! Please set it in environment variables.")
            sys.exit(1)
        
        logger.info("🤖 Initializing mrVXbBoT...")
        
        # Create application
        application = Application.builder().token(token).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("shorten", shorten_command))
        application.add_handler(CommandHandler("qr", qr_command))
        application.add_handler(CommandHandler("generate", generate_command))
        
        # Add message handlers
        application.add_handler(MessageHandler(filters.PHOTO, handle_image))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        
        # Add callback query handler for inline buttons
        application.add_handler(CallbackQueryHandler(handle_callback))
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        # Start the bot
        logger.info("🚀 Bot is starting and polling for updates...")
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
