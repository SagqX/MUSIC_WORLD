# Professional Telegram VCPlay Music Bot
# Main Entry Point

import asyncio
import logging
import time
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.input_stream import AudioPiped, VideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio, MediumQualityVideo
import config
from handlers import music_handlers, user_handlers, admin_handlers
from utils.database import Database
from utils.queue_manager import QueueManager
from utils.downloader import YouTubeDownloader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('musicbot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MusicBot:
    def __init__(self):
        # Store start time for uptime calculation
        self.start_time = time.time()
        
        # Initialize Pyrogram client
        self.app = Client(
            "musicbot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=config.SESSION_STRING
        )
        
        # Initialize PyTgCalls
        self.call_py = PyTgCalls(
            self.app,
            overload_quiet_mode=True
        )
        
        # Initialize bot client if bot token is provided
        if config.BOT_TOKEN:
            self.bot = Client(
                "musicbot_assistant",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                bot_token=config.BOT_TOKEN
            )
        else:
            self.bot = None
        
        # Initialize components
        self.db = Database()
        self.queue_manager = QueueManager()
        self.downloader = YouTubeDownloader()
        
        # Current playing status
        self.current_chat = None
        self.is_playing = False
        self.is_paused = False
        
        # Add handlers
        self._add_handlers()
    
    def _add_handlers(self):
        """Add all command and message handlers"""
        
        # Music commands
        @self.app.on_message(filters.command(["play", "p"]) & filters.group)
        async def play_command(client, message: Message):
            await music_handlers.play_handler(client, message, self)
        
        @self.app.on_message(filters.command(["vplay", "vp"]) & filters.group)
        async def vplay_command(client, message: Message):
            await music_handlers.vplay_handler(client, message, self)
        
        @self.app.on_message(filters.command(["pause"]) & filters.group)
        async def pause_command(client, message: Message):
            await music_handlers.pause_handler(client, message, self)
        
        @self.app.on_message(filters.command(["resume"]) & filters.group)
        async def resume_command(client, message: Message):
            await music_handlers.resume_handler(client, message, self)
        
        @self.app.on_message(filters.command(["skip", "next"]) & filters.group)
        async def skip_command(client, message: Message):
            await music_handlers.skip_handler(client, message, self)
        
        @self.app.on_message(filters.command(["stop", "end"]) & filters.group)
        async def stop_command(client, message: Message):
            await music_handlers.stop_handler(client, message, self)
        
        @self.app.on_message(filters.command(["queue", "q"]) & filters.group)
        async def queue_command(client, message: Message):
            await music_handlers.queue_handler(client, message, self)
        
        @self.app.on_message(filters.command(["shuffle"]) & filters.group)
        async def shuffle_command(client, message: Message):
            await music_handlers.shuffle_handler(client, message, self)
        
        @self.app.on_message(filters.command(["loop"]) & filters.group)
        async def loop_command(client, message: Message):
            await music_handlers.loop_handler(client, message, self)
        
        @self.app.on_message(filters.command(["volume", "vol"]) & filters.group)
        async def volume_command(client, message: Message):
            await music_handlers.volume_handler(client, message, self)
        
        @self.app.on_message(filters.command(["playlist", "pl"]) & filters.group)
        async def playlist_command(client, message: Message):
            await music_handlers.playlist_handler(client, message, self)
        
        @self.app.on_message(filters.command(["radio", "stream"]) & filters.group)
        async def radio_command(client, message: Message):
            await music_handlers.radio_handler(client, message, self)
        
        # Admin commands
        @self.app.on_message(filters.command(["reload"]) & filters.user(config.ADMINS))
        async def reload_command(client, message: Message):
            await admin_handlers.reload_handler(client, message, self)
        
        @self.app.on_message(filters.command(["logs"]) & filters.user(config.ADMINS))
        async def logs_command(client, message: Message):
            await admin_handlers.logs_handler(client, message, self)
        
        @self.app.on_message(filters.command(["speedtest"]) & filters.user(config.ADMINS))
        async def speedtest_command(client, message: Message):
            await admin_handlers.speedtest_handler(client, message, self)
        
        @self.app.on_message(filters.command(["broadcast"]) & filters.user(config.ADMINS))
        async def broadcast_command(client, message: Message):
            await user_handlers.broadcast_handler(client, message, self)
        
        @self.app.on_message(filters.command(["ban"]) & filters.user(config.ADMINS))
        async def ban_command(client, message: Message):
            await user_handlers.ban_user_handler(client, message, self)
        
        @self.app.on_message(filters.command(["unban"]) & filters.user(config.ADMINS))
        async def unban_command(client, message: Message):
            await user_handlers.unban_user_handler(client, message, self)
        
        @self.app.on_message(filters.command(["maintenance"]) & filters.user([config.OWNER_ID]))
        async def maintenance_command(client, message: Message):
            await user_handlers.maintenance_handler(client, message, self)
        
        @self.app.on_message(filters.command(["sysinfo"]) & filters.user(config.ADMINS))
        async def sysinfo_command(client, message: Message):
            await user_handlers.system_info_handler(client, message, self)
        
        # User commands
        @self.app.on_message(filters.command(["start", "help"]))
        async def start_command(client, message: Message):
            await user_handlers.start_handler(client, message, self)
        
        @self.app.on_message(filters.command(["ping"]))
        async def ping_command(client, message: Message):
            await user_handlers.ping_handler(client, message, self)
        
        @self.app.on_message(filters.command(["stats"]))
        async def stats_command(client, message: Message):
            await user_handlers.stats_handler(client, message, self)
        
        @self.app.on_message(filters.command(["about"]))
        async def about_command(client, message: Message):
            await user_handlers.about_handler(client, message, self)
        
        @self.app.on_message(filters.command(["language"]))
        async def language_command(client, message: Message):
            await user_handlers.language_handler(client, message, self)
        
        # PyTgCalls event handlers
        @self.call_py.on_stream_end()
        async def on_stream_end(client, update):
            await music_handlers.stream_end_handler(client, update, self)
        
        @self.call_py.on_closed_voice_chat()
        async def on_closed_vc(client, chat_id):
            await music_handlers.closed_vc_handler(client, chat_id, self)
        
        @self.call_py.on_kicked()
        async def on_kicked(client, chat_id):
            await music_handlers.kicked_handler(client, chat_id, self)
        
        @self.call_py.on_left()
        async def on_left(client, chat_id):
            await music_handlers.left_handler(client, chat_id, self)
    
    async def start(self):
        """Start the music bot"""
        try:
            await self.app.start()
            await self.call_py.start()
            
            if self.bot:
                await self.bot.start()
                logger.info("Bot assistant started successfully")
            
            # Initialize database
            await self.db.connect()
            
            logger.info("Music Bot started successfully!")
            logger.info(f"Bot username: @{self.app.me.username}")
            
            # Send startup message to log channel if configured
            if config.LOG_GROUP_ID:
                try:
                    import pyrogram
                    import pytgcalls
                    await self.app.send_message(
                        config.LOG_GROUP_ID,
                        f"🎵 **Music Bot Started Successfully!**\n\n"
                        f"**Bot Username:** @{self.app.me.username}\n"
                        f"**Pyrogram Version:** {pyrogram.__version__}\n"
                        f"**PyTgCalls Version:** {pytgcalls.__version__}\n"
                        f"**Status:** Online ✅"
                    )
                except Exception as e:
                    logger.error(f"Failed to send startup message: {e}")
            
            # Keep the bot running
            await self.app.idle()
            
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise
    
    async def stop(self):
        """Stop the music bot"""
        try:
            # Clear all queues
            self.queue_manager.clear_all()
            
            # Leave all voice chats
            if self.call_py.is_connected:
                await self.call_py.leave_group_call(self.current_chat)
            
            # Stop clients
            await self.call_py.stop()
            await self.app.stop()
            
            if self.bot:
                await self.bot.stop()
            
            # Close database
            await self.db.disconnect()
            
            logger.info("Music Bot stopped successfully!")
            
        except Exception as e:
            logger.error(f"Error stopping bot: {e}")

# Initialize and run the bot
async def main():
    bot = MusicBot()
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
