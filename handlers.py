"""
Command handlers for mrVXbBoT
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes
from utils import ImageUtils, URLUtils, ImageGenerator, is_valid_url, format_file_size
from config import Config
import io

logger = logging.getLogger(__name__)

# ========== START COMMAND ==========

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user = update.effective_user
    
    welcome_text = f"""
🚀 *Welcome to mrVXbBoT!* 

Hi {user.first_name}! 👋

I'm your all-in-one Telegram utility bot. Here's what I can do for you:

*📸 Image Tools*
• Convert images between formats
• Compress images to save space
• Get image information

*🔗 Link Tools*
• Shorten long URLs
• Generate QR codes

*🎨 AI Tools*
• Generate images from text descriptions

📌 *Quick Commands:*
/shorten [url] - Shorten a URL
/qr [text] - Generate a QR code
/generate [prompt] - Create AI art
/help - See detailed instructions

*Simply send me an image to get started!* 🎯
"""
    
    keyboard = [
        [
            InlineKeyboardButton("📸 Convert Image", callback_data='quick_convert'),
            InlineKeyboardButton("🔗 Shorten URL", callback_data='quick_shorten')
        ],
        [
            InlineKeyboardButton("🎨 Generate Image", callback_data='quick_generate'),
            InlineKeyboardButton("📱 QR Code", callback_data='quick_qr')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text, 
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

# ========== HELP COMMAND ==========

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    help_text = """
🤖 *mrVXbBoT - Complete Help Guide*

*📌 IMAGE CONVERTER*
Send any image and choose a format:
• PNG • JPEG • WEBP • BMP • GIF

*📌 URL SHORTENER*
/shorten <your_url>
Example: `/shorten https://example.com/very/long/url`

*📌 QR CODE GENERATOR*
/qr <text_or_url>
Example: `/qr https://t.me/mrVXbBoT`

*📌 AI IMAGE GENERATOR*
/generate <description>
Example: `/generate a beautiful sunset over mountains`

*📌 IMAGE COMPRESSION*
Send an image with caption "compress"

*📌 IMAGE INFORMATION*
Send an image with caption "info"

*⚡ PRO TIPS:*
• Use buttons below messages for quick actions
• I support most common image formats
• All processing is free and unlimited
• Your images are not stored permanently

*Need more help?* Contact @mrVXBoT_support 😊
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

# ========== SHORTEN COMMAND ==========

async def shorten_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /shorten command"""
    try:
        # Extract URL from command
        if context.args:
            url = context.args[0]
        else:
            text = update.message.text.replace('/shorten', '').strip()
            if not text:
                await update.message.reply_text(
                    "❌ Please provide a URL to shorten.\n"
                    "Example: `/shorten https://example.com`",
                    parse_mode='Markdown'
                )
                return
            url = text
        
        # Validate and format URL
        if not is_valid_url(url):
            await update.message.reply_text("❌ Invalid URL. Please include http:// or https://")
            return
        
        await update.message.reply_text("⏳ Shortening URL...")
        
        # Shorten URL
        short_url = URLUtils.shorten_url(url)
        
        response_text = f"""
✅ *URL Shortened Successfully!*

🔗 *Original:* {url}
✂️ *Shortened:* {short_url}

📊 *Stats:* Original length: {len(url)} → Shortened: {len(short_url)} characters
"""
        
        keyboard = [[
            InlineKeyboardButton("📋 Copy Link", callback_data=f'copy_{short_url}')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            response_text, 
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# ========== QR COMMAND ==========

async def qr_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /qr command"""
    try:
        # Extract text from command
        if context.args:
            text = ' '.join(context.args)
        else:
            text = update.message.text.replace('/qr', '').strip()
            if not text:
                await update.message.reply_text(
                    "❌ Please provide text or URL for the QR code.\n"
                    "Example: `/qr Hello World`",
                    parse_mode='Markdown'
                )
                return
        
        await update.message.reply_text("⏳ Generating QR code...")
        
        # Generate QR code
        qr_bytes = URLUtils.generate_qr(text)
        
        await update.message.reply_photo(
            photo=InputFile(qr_bytes, filename='qrcode.png'),
            caption=f"📱 *QR Code Generated!*\n\n🔗 *Content:* `{text}`",
            parse_mode='Markdown'
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# ========== GENERATE COMMAND ==========

async def generate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /generate command"""
    try:
        # Extract prompt from command
        if context.args:
            prompt = ' '.join(context.args)
        else:
            prompt = update.message.text.replace('/generate', '').strip()
            if not prompt:
                await update.message.reply_text(
                    "❌ Please provide a description for the image.\n"
                    "Example: `/generate a cute cat riding a bicycle`",
                    parse_mode='Markdown'
                )
                return
        
        await update.message.reply_text(
            f"🎨 *Generating image for:* `{prompt}`\n⏳ This may take a few seconds...",
            parse_mode='Markdown'
        )
        
        # Generate image
        image_bytes = ImageGenerator.generate_image(prompt)
        
        await update.message.reply_photo(
            photo=InputFile(image_bytes, filename='generated.png'),
            caption=f"🖼️ *AI Generated Image*\n\n📝 *Prompt:* `{prompt}`\n\n⚡ Powered by Pollinations.ai",
            parse_mode='Markdown'
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# ========== IMAGE HANDLER ==========

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle image messages"""
    try:
        user_id = update.effective_user.id
        photo = update.message.photo[-1]  # Get the largest photo
        caption = update.message.caption or ""
        
        # Download image
        file = await context.bot.get_file(photo.file_id)
        image_bytes = await file.download_as_bytearray()
        
        # Check file size
        if len(image_bytes) > Config.MAX_FILE_SIZE:
            await update.message.reply_text("❌ Image is too large. Maximum size is 20MB.")
            return
        
        # Store image in context
        context.user_data['last_image'] = image_bytes
        context.user_data['image_owner'] = user_id
        
        # Check for commands in caption
        if "compress" in caption.lower():
            await compress_image_handler(update, context, image_bytes)
            return
        elif "info" in caption.lower():
            await image_info_handler(update, context, image_bytes)
            return
        
        # Show conversion options
        keyboard = [
            [
                InlineKeyboardButton("🔵 PNG", callback_data=f'conv_png_{user_id}'),
                InlineKeyboardButton("🟢 JPG", callback_data=f'conv_jpg_{user_id}')
            ],
            [
                InlineKeyboardButton("🟣 WEBP", callback_data=f'conv_webp_{user_id}'),
                InlineKeyboardButton("🟡 BMP", callback_data=f'conv_bmp_{user_id}')
            ],
            [
                InlineKeyboardButton("🎨 GIF", callback_data=f'conv_gif_{user_id}')
            ],
            [
                InlineKeyboardButton("📦 Compress Image", callback_data=f'compress_{user_id}'),
                InlineKeyboardButton("ℹ️ Image Info", callback_data=f'info_{user_id}')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"📸 *Image received!* ({len(image_bytes)/1024:.1f} KB)\n\nWhat would you like to do with it?",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
    except Exception as e:
        logger.error(f"Image handler error: {e}")
        await update.message.reply_text(f"❌ Error processing image: {str(e)}")

# ========== COMPRESS IMAGE HANDLER ==========

async def compress_image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, image_bytes=None) -> None:
    """Compress an image"""
    try:
        if image_bytes is None:
            image_bytes = context.user_data.get('last_image')
            if not image_bytes:
                await update.message.reply_text("❌ No image found. Please send an image first.")
                return
        
        await update.message.reply_text("⏳ Compressing image...")
        
        # Compress image
        compressed = ImageUtils.compress_image(image_bytes)
        original_size = len(image_bytes)
        compressed_size = compressed.getbuffer().nbytes
        
        savings = original_size - compressed_size
        savings_percent = (savings / original_size) * 100 if original_size > 0 else 0
        
        await update.message.reply_photo(
            photo=InputFile(compressed, filename='compressed.jpg'),
            caption=f"""
✅ *Image Compressed Successfully!*

📊 *Original:* {format_file_size(original_size)}
📉 *Compressed:* {format_file_size(compressed_size)}
💾 *Saved:* {format_file_size(savings)} ({savings_percent:.1f}% reduction)
""",
            parse_mode='Markdown'
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Compression error: {str(e)}")

# ========== IMAGE INFO HANDLER ==========

async def image_info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, image_bytes=None) -> None:
    """Get image information"""
    try:
        if image_bytes is None:
            image_bytes = context.user_data.get('last_image')
            if not image_bytes:
                await update.message.reply_text("❌ No image found. Please send an image first.")
                return
        
        info = ImageUtils.get_image_info(image_bytes)
        
        info_text = f"""
ℹ️ *Image Information*

📐 *Dimensions:* {info['width']} × {info['height']} pixels
📦 *Format:* {info['format']}
🎨 *Color Mode:* {info['mode']}
📊 *File Size:* {format_file_size(info['size_kb'] * 1024)}
🔢 *Channels:* {info['channels']}
"""
        await update.message.reply_text(info_text, parse_mode='Markdown')
        
    except Exception as e:
        await update.message.reply_text(f"❌ Info error: {str(e)}")

# ========== TEXT HANDLER ==========

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages"""
    text = update.message.text.strip()
    
    # Check if it's a URL (for quick shortening)
    if text.startswith(('http://', 'https://')):
        context.args = [text]  # Trick to use shorten_command
        await shorten_command(update, context)
        return
    
    await update.message.reply_text(
        "🤔 I didn't understand that. Try these commands:\n\n"
        "🔹 /start - See what I can do\n"
        "🔹 /help - Get detailed instructions\n"
        "🔹 /shorten [url] - Shorten a URL\n"
        "🔹 /generate [prompt] - Generate an image\n"
        "🔹 /qr [text] - Generate a QR code\n\n"
        "💡 Or simply send me an image to get started!"
    )

# ========== CALLBACK HANDLER ==========

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline keyboard callbacks"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    data = query.data
    parts = data.split('_')
    action = parts[0]
    
    # Quick action handlers
    if action == 'quick':
        if 'convert' in data:
            await query.edit_message_text(
                "📸 Please send me the image you want to convert.\n\n"
                "I'll show you conversion options after you send it."
            )
        elif 'shorten' in data:
            await query.edit_message_text(
                "🔗 Please send the URL you want to shorten.\n\n"
                "Example: https://example.com/very/long/url"
            )
        elif 'generate' in data:
            await query.edit_message_text(
                "🎨 Please describe the image you want to generate.\n\n"
                "Example: a beautiful landscape with mountains and a lake"
            )
        elif 'qr' in data:
            await query.edit_message_text(
                "📱 Please send the text or URL for the QR code.\n\n"
                "Example: https://t.me/mrVXbBoT"
            )
        return
    
    # Copy link action
    if action == 'copy':
        short_url = data.replace('copy_', '')
        await query.edit_message_text(
            f"✅ Link copied to clipboard!\n\n"
            f"🔗 {short_url}"
        )
        return
    
    # Check if it's the right user for image operations
    if len(parts) > 1 and parts[-1].isdigit():
        owner_id = int(parts[-1])
        if owner_id != user_id:
            await query.edit_message_text(
                "❌ This action is not for you. Please send your own image first."
            )
            return
    
    # Image conversion
    if action == 'conv':
        target_format = parts[1].upper()
        image_bytes = context.user_data.get('last_image')
        
        if not image_bytes:
            await query.edit_message_text("❌ No image found. Please send an image first.")
            return
        
        await query.edit_message_text(f"⏳ Converting to {target_format}...")
        
        try:
            converted = ImageUtils.convert_image(image_bytes, target_format)
            await update.effective_chat.send_photo(
                photo=InputFile(converted, filename=f'converted.{target_format.lower()}'),
                caption=f"✅ *Converted to {target_format} successfully!*",
                parse_mode='Markdown'
            )
        except Exception as e:
            await query.edit_message_text(f"❌ Conversion error: {str(e)}")
        return
    
    # Compress action
    if action == 'compress':
        image_bytes = context.user_data.get('last_image')
        if not image_bytes:
            await query.edit_message_text("❌ No image found. Please send an image first.")
            return
        await compress_image_handler(update, context, image_bytes)
        await query.delete_message()
        return
    
    # Info action
    if action == 'info':
        image_bytes = context.user_data.get('last_image')
        if not image_bytes:
            await query.edit_message_text("❌ No image found. Please send an image first.")
            return
        await image_info_handler(update, context, image_bytes)
        await query.delete_message()
        return

# ========== ERROR HANDLER ==========

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    
    try:
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ An error occurred. Please try again later."
            )
    except:
        pass
