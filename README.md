# 🤖 mrVXbBoT - All-in-One Telegram Utility Bot

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/YOUR_TEMPLATE)

A powerful, feature-rich Telegram bot that provides essential utility functions including image conversion, URL shortening, QR code generation, and AI-powered image creation.

## ✨ Features

### 📸 Image Tools
- **Convert Images**: Convert between PNG, JPG, WEBP, BMP, GIF formats
- **Compress Images**: Reduce file size while maintaining quality
- **Image Info**: Get dimensions, format, size, and color mode

### 🔗 Link Tools
- **URL Shortener**: Shorten long URLs instantly
- **QR Code Generator**: Create QR codes from text or URLs

### 🎨 AI Tools
- **AI Image Generator**: Create images from text descriptions using free AI API

## 🚀 Quick Deploy to Railway

1. **Fork this repository** to your GitHub account

2. **Create bot on Telegram**:
   - Message @BotFather
   - Send `/newbot`
   - Set name: `mrVXbBoT`
   - Set username: `mrVXbBoT`
   - Copy the token

3. **Deploy on Railway**:
   - Go to [Railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your forked repository
   - Add environment variable:
     - Key: `BOT_TOKEN`
     - Value: (paste your bot token)

4. **Deploy**: Railway will automatically build and deploy your bot

## 📋 Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Welcome message with quick actions | `/start` |
| `/help` | Detailed help guide | `/help` |
| `/shorten [url]` | Shorten a URL | `/shorten https://example.com` |
| `/qr [text]` | Generate QR code | `/qr Hello World` |
| `/generate [prompt]` | Generate AI image | `/generate a cat in space` |

## 🛠️ Local Development

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
4. Install dependencies: `pip install -r requirements.txt`
5. Set environment variables: `cp .env.example .env` and add your BOT_TOKEN
6. Run: `python bot.py`

## 📝 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BOT_TOKEN` | Your bot token from @BotFather | ✅ Yes |
| `LOG_LEVEL` | Logging level (INFO, DEBUG, ERROR) | ❌ No |

---

Made with ❤️ for the Telegram community
