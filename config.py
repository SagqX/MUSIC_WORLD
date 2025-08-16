# Configuration file for Telegram Music Bot
import os
from typing import List

# Bot Configuration
API_ID: int = int(os.getenv("API_ID", "12345678"))
API_HASH: str = os.getenv("API_HASH", "your_api_hash_here")
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")  # Optional: for assistant bot
SESSION_STRING: str = os.getenv("SESSION_STRING", "your_session_string_here")

# Admin Configuration
ADMINS: List[int] = [int(x) for x in os.getenv("ADMINS", "").split() if x.isdigit()]
OWNER_ID: int = int(os.getenv("OWNER_ID", "0"))
if OWNER_ID not in ADMINS:
    ADMINS.append(OWNER_ID)

# Group Configuration
LOG_GROUP_ID: int = int(os.getenv("LOG_GROUP_ID", "0"))
MUSIC_BOT_NAME: str = os.getenv("MUSIC_BOT_NAME", "VCPlay Music Bot")

# Audio & Video Quality
AUDIO_QUALITY: str = os.getenv("AUDIO_QUALITY", "high")  # low, medium, high
VIDEO_QUALITY: str = os.getenv("VIDEO_QUALITY", "medium")  # low, medium, high
BITRATE: int = int(os.getenv("BITRATE", "512"))

# Features Configuration
AUTO_LEAVE: bool = os.getenv("AUTO_LEAVE", "True").lower() in ["true", "1", "yes"]
AUTO_LEAVE_DURATION: int = int(os.getenv("AUTO_LEAVE_DURATION", "300"))  # 5 minutes
MAX_QUEUE_SIZE: int = int(os.getenv("MAX_QUEUE_SIZE", "50"))
MAX_DURATION_LIMIT: int = int(os.getenv("MAX_DURATION_LIMIT", "3600"))  # 1 hour in seconds
PLAYLIST_LIMIT: int = int(os.getenv("PLAYLIST_LIMIT", "25"))

# Download Configuration
DOWNLOAD_DIR: str = os.getenv("DOWNLOAD_DIR", "downloads")
CLEANUP_DOWNLOADS: bool = os.getenv("CLEANUP_DOWNLOADS", "True").lower() in ["true", "1", "yes"]
CLEANUP_INTERVAL: int = int(os.getenv("CLEANUP_INTERVAL", "300"))  # 5 minutes

# Language Configuration
DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "en")

# Database Configuration (MongoDB)
MONGO_DB_URI: str = os.getenv("MONGO_DB_URI", "")
DB_NAME: str = os.getenv("DB_NAME", "musicbot")

# Spotify Configuration (Optional)
SPOTIFY_CLIENT_ID: str = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET: str = os.getenv("SPOTIFY_CLIENT_SECRET", "")

# Last.fm Configuration (Optional)
LASTFM_API_KEY: str = os.getenv("LASTFM_API_KEY", "")
LASTFM_SECRET: str = os.getenv("LASTFM_SECRET", "")

# YouTube Configuration
YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")  # Optional for better search results

# Thumbnail Configuration
THUMBNAIL_URL: str = os.getenv("THUMBNAIL_URL", "https://telegra.ph/file/c6e1040897f8b2f6dbde0.jpg")
DURATION_LIMIT_MIN: int = int(os.getenv("DURATION_LIMIT_MIN", "60"))  # minutes

# Command Prefixes
COMMAND_PREFIXES: List[str] = os.getenv("COMMAND_PREFIXES", "/ ! . ?").split()

# Auto-generated directories
CACHE_DIR = "cache"
LOGS_DIR = "logs"

# Create necessary directories
for directory in [DOWNLOAD_DIR, CACHE_DIR, LOGS_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Supported formats
AUDIO_FORMATS = [
    "mp3", "wav", "flac", "m4a", "aac", "ogg", "wma", "opus"
]

VIDEO_FORMATS = [
    "mp4", "mkv", "avi", "mov", "wmv", "flv", "webm", "3gp"
]

# YouTube-dl options
YTDL_OPTS = {
    "format": "best[height<=720]/best",
    "extractaudio": True,
    "audioformat": "mp3",
    "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "extractflat": True,
    "writesubtitles": False,
    "writeautomaticsub": False,
}

# FFmpeg options
FFMPEG_OPTS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn -filter:a volume=0.8"
}

# Radio stations (example)
RADIO_STATIONS = {
    "lofi": "https://www.youtube.com/watch?v=jfKfPfyJRdk",
    "chill": "https://www.youtube.com/watch?v=5qap5aO4i9A",
    "jazz": "https://www.youtube.com/watch?v=DSGyEsJ17cI",
    "classical": "https://www.youtube.com/watch?v=vCNg-RzOwJM"
}

# Special features configuration
GENIUS_API_TOKEN: str = os.getenv("GENIUS_API_TOKEN", "")  # For lyrics
WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")  # For weather commands
NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")  # For news commands

# Heroku Configuration
HEROKU_APP_NAME: str = os.getenv("HEROKU_APP_NAME", "")
HEROKU_API_KEY: str = os.getenv("HEROKU_API_KEY", "")

# Upstream repository
UPSTREAM_REPO: str = "https://github.com/YourUsername/VCPlayMusicBot"
UPSTREAM_BRANCH: str = "main"

# Version
__version__ = "2.0.0"

# Help text
HELP_TEXT = f"""
🎵 **{MUSIC_BOT_NAME} Commands** 🎵

**🎶 Music Commands:**
• `/play` or `/p` [song name/link] - Play audio in voice chat
• `/vplay` or `/vp` [video name/link] - Play video in voice chat
• `/pause` - Pause current stream
• `/resume` - Resume paused stream
• `/skip` or `/next` - Skip current track
• `/stop` or `/end` - Stop playing and clear queue
• `/queue` or `/q` - Show current queue
• `/shuffle` - Shuffle queue
• `/loop` - Toggle loop mode
• `/volume` [1-100] - Adjust volume
• `/playlist` [url] - Play entire playlist
• `/radio` [station/url] - Play radio stream

**📊 Information Commands:**
• `/ping` - Check bot latency
• `/stats` - Show bot statistics
• `/help` - Show this help message

**👮‍♂️ Admin Commands:**
• `/reload` - Reload bot configurations
• `/logs` - Get bot logs
• `/speedtest` - Test server speed

**🎵 Special Features:**
• Auto-queue management
• High-quality audio streaming
• Video streaming support
• Playlist support (YouTube, Spotify)
• Radio station streaming
• Multiple language support
• Advanced queue controls

**💝 Powered by PyTgCalls & Pyrogram**
**Version:** {__version__}
"""

# Validate configuration
if not API_ID or not API_HASH:
    raise ValueError("API_ID and API_HASH must be provided")

if not SESSION_STRING:
    raise ValueError("SESSION_STRING must be provided")

if not ADMINS:
    raise ValueError("At least one ADMIN must be provided")
