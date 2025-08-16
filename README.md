## 2. README.md ( Full Script)


# 🎵 VCPlay Music Bot - Professional Telegram Voice Chat Music Bot

A powerful, feature-rich Telegram music bot built with **Pyrogram** and **PyTgCalls** for high-quality audio and video streaming in voice chats.

[![GitHub stars](https://img.shields.io/github/stars/YourUsername/VCPlayMusicBot?style=social)](https://github.com/YourUsername/VCPlayMusicBot/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/YourUsername/VCPlayMusicBot?style=social)](https://github.com/YourUsername/VCPlayMusicBot/network/members)
[![GitHub issues](https://img.shields.io/github/issues/YourUsername/VCPlayMusicBot)](https://github.com/YourUsername/VCPlayMusicBot/issues)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ Key Features

### 🎶 Music Streaming
- **High-quality audio streaming** (up to 320kbps)
- **Video streaming support** (up to 720p)
- **YouTube integration** with search and direct links
- **Spotify track support** with YouTube fallback
- **Radio streaming** from live streams
- **Local file playback** (audio/video files)
- **Multiple format support** (MP3, FLAC, M4A, WAV, etc.)

### 🎛️ Advanced Controls
- **Queue management** with shuffle, loop, skip
- **Volume control** (1-100%)
- **Pause/Resume** functionality  
- **Playlist support** (YouTube playlists)
- **Auto-queue** from playlists
- **Multiple chat support** (different queues per chat)
- **Seek functionality** (jump to specific time)
- **Repeat modes** (off, single, all)

### 🔧 Administrative Features
- **Admin-only mode** for restricted usage
- **User management** (ban/unban system)
- **Statistics tracking** and analytics
- **Automated cleanup** of temporary files
- **Logging system** with rotation
- **Database integration** (MongoDB)
- **Broadcast system** for announcements
- **Speed testing** for server performance

### 🌐 Special Features
- **Multi-language support** (English, Hindi, Spanish, French, etc.)
- **Inline keyboard controls**
- **Real-time now playing** updates
- **Download progress tracking**
- **Auto-leave** when voice chat is empty
- **Thumbnail generation**
- **Lyrics display** (with Genius API)
- **Cross-platform compatibility**

## 📋 Requirements

- **Python 3.9+** (3.11 recommended)
- **FFmpeg** (for audio/video processing)
- **MongoDB** (optional, for database features)
- **Telegram API credentials**
- **VPS/Server** (recommended for 24/7 hosting)
- **Minimum 1GB RAM** (2GB+ recommended)
- **Stable internet connection** (10+ Mbps upload)

## 🚀 Installation Guide

### 1. Clone the Repository

```
git clone https://github.com/YourUsername/VCPlayMusicBot.git
cd VCPlayMusicBot
```

### 2. Install System Dependencies

#### Ubuntu/Debian:
```
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv ffmpeg git curl -y
```

#### CentOS/RHEL:
```
sudo yum update -y
sudo yum install python3 python3-pip ffmpeg git curl -y
```

#### Arch Linux:
```
sudo pacman -Sy python python-pip ffmpeg git curl
```

### 3. Create Virtual Environment

```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Python Dependencies

```
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Generate Session String

Create `generate_session.py`:

```
from pyrogram import Client

API_ID = int(input("Enter your API_ID: "))
API_HASH = input("Enter your API_HASH: ")

print("Generating session string...")

with Client("session", API_ID, API_HASH) as app:
    session_string = app.export_session_string()
    print(f"\nYour session string:\n{session_string}")
    print("\n⚠️ Keep this session string secure!")
```

Run it:
```
python generate_session.py
```

### 6. Configure the Bot

Copy and edit configuration:
```
cp .env.example .env
# Edit .env with your credentials
```

Or edit `config.py` directly:

```
# Essential Configuration
API_ID = 12345678  # Get from my.telegram.org
API_HASH = "your_api_hash_here"
SESSION_STRING = "your_session_string_here"
BOT_TOKEN = "your_bot_token_here"  # Optional

# Admin Configuration  
ADMINS = [123456789][987654321]  # Your user IDs
OWNER_ID = 123456789  # Owner user ID
LOG_GROUP_ID = -1001234567890  # Log group ID (optional)

# Database (Optional but recommended)
MONGO_DB_URI = "mongodb://localhost:27017"
DB_NAME = "musicbot"

# Quality Settings
AUDIO_QUALITY = "high"  # low, medium, high
VIDEO_QUALITY = "medium"  # low, medium, high
MAX_DURATION_LIMIT = 3600  # 1 hour in seconds
PLAYLIST_LIMIT = 25  # Max songs from playlist
```

### 7. Run the Bot

```
python main.py
```

## 📱 Bot Commands

### 🎵 Music Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/play` or `/p` | Play audio in voice chat | `/play Imagine Dragons Believer` |
| `/vplay` or `/vp` | Play video in voice chat | `/vplay Ed Sheeran Shape of You` |
| `/pause` | Pause current stream | `/pause` |
| `/resume` | Resume paused stream | `/resume` |
| `/skip` or `/next` | Skip current track | `/skip` |
| `/stop` or `/end` | Stop playing and clear queue | `/stop` |
| `/queue` or `/q` | Show current queue | `/queue` |
| `/shuffle` | Shuffle queue | `/shuffle` |
| `/loop` | Toggle loop mode | `/loop` |
| `/volume` or `/vol` | Adjust volume (1-100) | `/volume 75` |
| `/playlist` or `/pl` | Play YouTube playlist | `/playlist https://youtube.com/playlist?list=...` |
| `/radio` or `/stream` | Play radio stream | `/radio lofi` |

### 📊 Information Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/start` | Show welcome message | `/start` |
| `/help` | Display help message | `/help` |
| `/ping` | Check bot latency | `/ping` |
| `/stats` | Show bot statistics | `/stats` |
| `/about` | Bot information | `/about` |
| `/language` | Change language | `/language` |

### 👮‍♂️ Admin Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/reload` | Reload bot configurations | `/reload` |
| `/logs` | Get bot logs | `/logs` |
| `/speedtest` | Test server speed | `/speedtest` |
| `/broadcast` | Broadcast message | `/broadcast` (reply to message) |
| `/ban` | Ban user from bot | `/ban 123456789` |
| `/unban` | Unban user | `/unban 123456789` |
| `/maintenance` | Run maintenance tasks | `/maintenance` |
| `/sysinfo` | System information | `/sysinfo` |

### 🎧 Advanced Features

- **Reply to audio file** with `/play` to play it directly
- **YouTube/Spotify links** work directly with `/play`
- **Live stream URLs** supported with `/radio`
- **Multiple quality options** for audio and video
- **Auto-download and cleanup** of temporary files
- **Smart queue management** with position tracking

## 🐳 Deployment Options

### Option 1: Heroku (One-Click Deploy)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/YourUsername/VCPlayMusicBot)

1. Click the deploy button above
2. Fill in the required environment variables
3. Deploy and enable worker dyno

### Option 2: Docker Deployment

#### Using Docker Compose

1. Create `.env` file with your configuration:

```
API_ID=12345678
API_HASH=your_api_hash_here
SESSION_STRING=your_session_string_here
ADMINS=123456789 987654321
OWNER_ID=123456789
MONGO_DB_URI=mongodb://mongodb:27017/musicbot
```

2. Run with Docker Compose:

```
docker-compose up -d
```

#### Manual Docker Build

```
docker build -t vcplay-musicbot .
docker run -d --name musicbot --env-file .env vcplay-musicbot
```

### Option 3: Railway Deployment

1. Fork this repository
2. Connect to [Railway](https://railway.app)
3. Set environment variables
4. Deploy

### Option 4: VPS Deployment

#### Automated Installation

```
curl -O https://raw.githubusercontent.com/YourUsername/VCPlayMusicBot/main/scripts/install.sh
chmod +x install.sh
./install.sh
```

#### Manual VPS Setup

```
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3 python3-pip python3-venv ffmpeg git curl -y

# Clone and setup
git clone https://github.com/YourUsername/VCPlayMusicBot.git
cd VCPlayMusicBot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your credentials

# Run
python main.py
```

#### Systemd Service (Linux)

Create service file:
```
sudo nano /etc/systemd/system/vcplay-musicbot.service
```

```
[Unit]
Description=VCPlay Music Bot
After=network.target

[Service]
Type=simple
User=musicbot
WorkingDirectory=/home/musicbot/VCPlayMusicBot
ExecStart=/home/musicbot/VCPlayMusicBot/venv/bin/python main.py
Restart=always
RestartSec=10
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

Enable and start:
```
sudo systemctl daemon-reload
sudo systemctl enable vcplay-musicbot
sudo systemctl start vcplay-musicbot
```

## 🔒 Security & Permissions

### Required Bot Permissions

When adding to a group, ensure the bot has:
- ✅ **Delete messages**
- ✅ **Manage voice chats**  
- ✅ **Send messages**
- ✅ **Send media**
- ✅ **Add users**
- ✅ **Read message history**

### User Account Requirements

The session string account must:
- ✅ **Be admin** in the target group
- ✅ **Have voice chat permissions**
- ✅ **Not be restricted**
- ⚠️ **2FA disabled** (recommended for stability)

### Security Best Practices

- 🔐 Keep session strings and tokens secure
- 🚫 Never share credentials publicly
- 🔄 Rotate credentials regularly
- 📊 Monitor bot logs for suspicious activity
- 🛡️ Use environment variables for sensitive data

## 🛠️ Configuration Options

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `API_ID` | Telegram API ID | - | ✅ |
| `API_HASH` | Telegram API Hash | - | ✅ |
| `SESSION_STRING` | Pyrogram session | - | ✅ |
| `BOT_TOKEN` | Bot token (optional) | - | ❌ |
| `ADMINS` | Admin user IDs (space-separated) | - | ✅ |
| `OWNER_ID` | Owner user ID | - | ✅ |
| `LOG_GROUP_ID` | Log group ID | 0 | ❌ |
| `MONGO_DB_URI` | MongoDB connection string | - | ❌ |
| `AUDIO_QUALITY` | Audio quality (low/medium/high) | high | ❌ |
| `VIDEO_QUALITY` | Video quality (low/medium/high) | medium | ❌ |
| `MAX_DURATION_LIMIT` | Max song duration (seconds) | 3600 | ❌ |
| `PLAYLIST_LIMIT` | Max playlist songs | 25 | ❌ |
| `AUTO_LEAVE` | Auto-leave empty chats | True | ❌ |
| `CLEANUP_DOWNLOADS` | Auto-cleanup downloads | True | ❌ |

### Advanced Configuration

```
# Quality Settings
AUDIO_QUALITY = "high"  # low, medium, high
VIDEO_QUALITY = "medium"  # low, medium, high
BITRATE = 512  # Audio bitrate in kbps

# Feature Toggles
AUTO_LEAVE = True  # Leave empty voice chats
AUTO_LEAVE_DURATION = 300  # 5 minutes
CLEANUP_DOWNLOADS = True  # Auto-cleanup files
CLEANUP_INTERVAL = 300  # Cleanup interval

# Limits
MAX_QUEUE_SIZE = 50  # Maximum songs in queue
MAX_DURATION_LIMIT = 3600  # 1 hour max duration
PLAYLIST_LIMIT = 25  # Max songs from playlists

# API Keys (Optional)
SPOTIFY_CLIENT_ID = "your_spotify_id"
SPOTIFY_CLIENT_SECRET = "your_spotify_secret"
GENIUS_API_TOKEN = "your_genius_token"
LASTFM_API_KEY = "your_lastfm_key"

# Heroku Configuration (if deploying to Heroku)
HEROKU_APP_NAME = "your-app-name"
HEROKU_API_KEY = "your-heroku-api-key"
```

## 🧪 Testing

### Unit Tests

```
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
python -m pytest tests/ -v
```

### Manual Testing

```
# Test imports
python -c "import main; print('✅ Imports OK')"

# Test configuration
python -c "import config; print('✅ Config OK')"

# Test database connection
python -c "from utils.database import Database; print('✅ Database OK')"
```

## 🐛 Troubleshooting

### Common Issues & Solutions

**1. "No module named 'pyrogram'"**
```
# Solution: Install dependencies
pip install -r requirements.txt
```

**2. "FFmpeg not found"**
```
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows (use Chocolatey)
choco install ffmpeg
```

**3. "Session string invalid"**
```
# Solution: Generate new session string
python generate_session.py
```

**4. "Permission denied" in voice chat**
```
# Solution: Make bot admin with voice chat permissions
# Also ensure userbot account is admin
```

**5. "No active voice chat found"**
```
# Solution: Start voice chat in group first
# Then use music commands
```

**6. "Download failed" errors**
```
# Check internet connection
# Verify YouTube accessibility
# Update yt-dlp: pip install -U yt-dlp
```

### Performance Optimization

**Server Requirements:**
- **Minimum:** 1 CPU core, 1GB RAM, 10GB storage
- **Recommended:** 2 CPU cores, 2GB RAM, 20GB storage
- **High-load:** 4 CPU cores, 4GB RAM, 50GB+ storage

**Network Requirements:**
- **Minimum:** 5 Mbps upload/download
- **Recommended:** 10+ Mbps upload/download
- **Low latency** to Telegram servers

**Optimization Tips:**
- Use SSD storage for faster file operations
- Enable download cleanup to save space
- Use MongoDB for better performance with multiple chats
- Monitor system resources with `/sysinfo`
- Use CDN for thumbnail hosting

### Debug Mode

Enable debug logging:
```
# In config.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Log Analysis

View real-time logs:
```
tail -f musicbot.log
```

Filter error logs:
```
grep -i error musicbot.log
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Development Setup

1. **Fork and clone:**
```
git clone https://github.com/YourUsername/VCPlayMusicBot.git
cd VCPlayMusicBot
git checkout -b feature-branch
```

2. **Install dev dependencies:**

```
pip install -r requirements-dev.txt
```

3. **Make changes and test:**

# Run tests

```
python -m pytest
```
# Format code
black .
flake8 .

4. **Submit pull request**

### Contribution Guidelines

- 📝 Write clear commit messages
- 🧪 Add tests for new features
- 📚 Update documentation
- 🎨 Follow code style guidelines
- 🐛 Fix bugs and improve performance

### Areas for Contribution

- 🌐 **Translations** (add more languages)
- 🎵 **Music sources** (add more platforms)
- 🔧 **Features** (new commands and functionality)
- 🐛 **Bug fixes** (report and fix issues)
- 📚 **Documentation** (improve guides and docs)
- 🧪 **Testing** (write more tests)

## 📊 Project Statistics

- **Language:** Python 3.11+
- **Framework:** Pyrogram + PyTgCalls
- **Database:** MongoDB (optional)
- **Audio Processing:** FFmpeg
- **Code Quality:** Black, Flake8
- **Testing:** Pytest
- **Documentation:** Markdown
- **Deployment:** Docker, Heroku, VPS

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.


MIT License

Copyright (c) 2025 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


## 🆘 Support & Community

### Get Help

- **Telegram Support Group:** [@VCPlayMusicBotSupport](https://t.me/VCPlayMusicBotSupport)
- **Updates Channel:** [@VCPlayMusicBotUpdates](https://t.me/VCPlayMusicBotUpdates)
- **GitHub Issues:** [Report Bug/Request Feature](https://github.com/YourUsername/VCPlayMusicBot/issues)
- **Documentation Wiki:** [Detailed Guides](https://github.com/YourUsername/VCPlayMusicBot/wiki)

### Community Guidelines

- 🤝 **Be respectful** and helpful to others
- 🐛 **Report bugs** with detailed information
- 💡 **Suggest features** constructively
- 📚 **Share knowledge** and help newcomers
- 🚫 **No spam** or off-topic discussions

### Frequently Asked Questions

<details>
<summary><strong>Can I use a regular bot account?</strong></summary>

No, you must use a user account (userbot) for voice chat functionality. Regular bot accounts cannot join voice chats.
</details>

<details>
<summary><strong>Is this bot free to use?</strong></summary>

Yes, the bot is completely free and open-source. However, you'll need to provide your own server/hosting.
</details>

<details>
<summary><strong>Can I modify the source code?</strong></summary>

Yes, under the MIT license, you can freely modify, distribute, and use the code for any purpose.
</details>

<details>
<summary><strong>Does it support multiple groups?</strong></summary>

Yes, the bot can handle multiple groups simultaneously with separate queues for each.
</details>

<details>
<summary><strong>What music sources are supported?</strong></summary>

Currently supports YouTube (primary), Spotify (via YouTube search), radio streams, and local files. More sources can be added.
</details>

## 🌟 Acknowledgments

Special thanks to:

- **[Dan](https://github.com/delivrance)** - Creator of Pyrogram
- **[Laky-64](https://github.com/Laky-64)** - Developer of PyTgCalls  
- **[yt-dlp team](https://github.com/yt-dlp/yt-dlp)** - YouTube downloading library
- **[FFmpeg team](https://ffmpeg.org/)** - Media processing framework
- **All contributors** who helped improve this project
- **Community members** for testing and feedback

## 📈 Statistics & Analytics

![GitHub Stats](https://github-readme-stats.vercel.app/api/pin/?username=YourUsername&repo=VCPlayMusicBot&theme=dark)

### Project Metrics

- ⭐ **GitHub Stars:** ![GitHub stars](https://img.shields.io/github/stars/YourUsername/VCPlayMusicBot)
- 🍴 **Forks:** ![GitHub forks](https://img.shields.io/github/forks/YourUsername/VCPlayMusicBot)
- 🐛 **Issues:** ![GitHub issues](https://img.shields.io/github/issues/YourUsername/VCPlayMusicBot)
- 📥 **Downloads:** ![GitHub downloads](https://img.shields.io/github/downloads/YourUsername/VCPlayMusicBot/total)
- 💾 **Code Size:** ![GitHub code size](https://img.shields.io/github/languages/code-size/YourUsername/VCPlayMusicBot)
- 📝 **Lines of Code:** ![Lines of code](https://img.shields.io/tokei/lines/github/YourUsername/VCPlayMusicBot)

## 🚀 Roadmap & Future Plans

### Version 2.1 (Next Release)
- [ ] **AI-powered music recommendations**
- [ ] **Lyrics display with synchronized highlighting**
- [ ] **Voice commands support**
- [ ] **Mobile app companion**

### Version 2.2 (Planned)
- [ ] **Web dashboard for management**
- [ ] **Advanced analytics and insights**
- [ ] **Multi-server load balancing**
- [ ] **Custom bot branding options**

### Version 3.0 (Long-term)
- [ ] **Plugin system for extensions**
- [ ] **Advanced audio effects and filters**
- [ ] **Live streaming to multiple platforms**
- [ ] **Enterprise features and scaling**

---

## 💝 Show Your Support

If you find this project helpful, please consider:

- ⭐ **Starring this repository**
- 🐛 **Reporting bugs and issues**
- 💡 **Suggesting new features**
- 🤝 **Contributing code improvements**
- 💰 **Supporting development**

### Support Development

[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/yourusername)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/yourusername)
[![GitHub Sponsors](https://img.shields.io/badge/sponsor-30363D?style=for-the-badge&logo=GitHub-Sponsors&logoColor=#EA4AAA)](https://github.com/sponsors/YourUsername)

---

**⭐ Don't forget to star this repository if you found it helpful!**

**Made with ❤️ by [Your Name](https://github.com/YourUsername)**

---

*Last updated: August 16, 2025*
