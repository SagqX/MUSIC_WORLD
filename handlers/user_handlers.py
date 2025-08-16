# User and Admin command handlers for VCPlay Music Bot

import asyncio
import time
import psutil
import platform
import pyrogram
import pytgcalls
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import config
from utils.helpers import get_readable_time, humanbytes

# User command handlers

async def start_handler(client: Client, message: Message, bot):
    """Handle /start and /help commands"""
    user = message.from_user
    
    # Add user to database
    await bot.db.add_user(user.id, user.username or "", user.first_name or "")
    
    # Check if user is banned
    if await bot.db.is_user_banned(user.id):
        return await message.reply_text(
            "❌ **You are banned from using this bot!**\n\n"
            "Contact the bot owner if you think this is a mistake."
        )
    
    if message.chat.type == "private":
        # Private chat - show full help
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("➕ Add to Group", url=f"https://t.me/{client.me.username}?startgroup=true"),
                InlineKeyboardButton("📢 Updates", url="https://t.me/your_channel")
            ],
            [
                InlineKeyboardButton("💡 Commands", callback_data="help_commands"),
                InlineKeyboardButton("ℹ️ About", callback_data="help_about")
            ],
            [
                InlineKeyboardButton("📊 Statistics", callback_data="stats_global"),
                InlineKeyboardButton("⚙️ Settings", callback_data="user_settings")
            ]
        ])
        
        await message.reply_photo(
            config.THUMBNAIL_URL,
            caption=f"🎵 **Welcome to {config.MUSIC_BOT_NAME}!**\n\n"
                   f"**Hello {user.first_name}!** I'm a powerful music bot that can play high-quality audio and video in Telegram voice chats.\n\n"
                   f"**🎯 Key Features:**\n"
                   f"• High-quality audio streaming\n"
                   f"• Video streaming support\n"
                   f"• YouTube, Spotify integration\n"
                   f"• Advanced queue management\n"
                   f"• Playlist support\n"
                   f"• Radio streaming\n"
                   f"• Multiple language support\n\n"
                   f"**📖 Quick Start:**\n"
                   f"1. Add me to your group\n"
                   f"2. Make me admin with voice chat permissions\n"
                   f"3. Start a voice chat\n"
                   f"4. Use `/play [song name]` to play music\n\n"
                   f"**🔗 Add me to your group and start enjoying music!**",
            reply_markup=keyboard
        )
    else:
        # Group chat - show brief help
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📖 Full Guide", url=f"https://t.me/{client.me.username}?start=help"),
                InlineKeyboardButton("💡 Commands", callback_data="help_commands")
            ]
        ])
        
        await message.reply_text(
            f"👋 **Hello {user.first_name}!**\n\n"
            f"I'm {config.MUSIC_BOT_NAME}, ready to play music in your voice chat!\n\n"
            f"**🎵 Quick Commands:**\n"
            f"• `/play [song name]` - Play audio\n"
            f"• `/vplay [video name]` - Play video\n"
            f"• `/queue` - Show queue\n"
            f"• `/skip` - Skip current song\n"
            f"• `/pause` - Pause playback\n"
            f"• `/resume` - Resume playback\n\n"
            f"**💡 Tip:** Start a voice chat first, then use commands!",
            reply_markup=keyboard
        )

async def ping_handler(client: Client, message: Message, bot):
    """Handle /ping command"""
    start_time = time.time()
    ping_msg = await message.reply_text("🏃‍♂️ **Pinging...**")
    end_time = time.time()
    
    # Calculate latencies
    telegram_latency = round((end_time - start_time) * 1000, 2)
    
    # Get system info
    try:
        uptime = get_readable_time(time.time() - psutil.boot_time())
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
    except:
        uptime = "Unknown"
        cpu_usage = 0
        memory = type('obj', (object,), {'percent': 0, 'used': 0, 'total': 0})
        disk = type('obj', (object,), {'percent': 0, 'used': 0, 'total': 0})
    
    # Bot uptime (simplified)
    bot_uptime = get_readable_time(time.time() - getattr(bot, 'start_time', time.time()))
    
    ping_text = f"🏓 **Pong!**\n\n" \
                f"**📡 Latency:** `{telegram_latency}ms`\n" \
                f"**⏱ Bot Uptime:** `{bot_uptime}`\n" \
                f"**🖥 System Uptime:** `{uptime}`\n\n" \
                f"**💻 System Stats:**\n" \
                f"**CPU Usage:** `{cpu_usage}%`\n" \
                f"**Memory:** `{memory.percent}%` ({humanbytes(memory.used)}/{humanbytes(memory.total)})\n" \
                f"**Disk:** `{disk.percent}%` ({humanbytes(disk.used)}/{humanbytes(disk.total)})\n\n" \
                f"**🎵 Music Status:**\n" \
                f"**Playing:** `{'Yes' if bot.is_playing else 'No'}`\n" \
                f"**Paused:** `{'Yes' if bot.is_paused else 'No'}`\n" \
                f"**Active Chats:** `{len(bot.queue_manager.queues)}`"
    
    await ping_msg.edit_text(ping_text)

async def stats_handler(client: Client, message: Message, bot):
    """Handle /stats command"""
    # Get global stats from database
    global_stats = await bot.db.get_global_stats()
    
    # Get queue manager stats
    queue_stats = bot.queue_manager.get_queue_stats()
    
    # Get system stats
    try:
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
    except:
        memory = type('obj', (object,), {'percent': 0})
        disk = type('obj', (object,), {'percent': 0})
    
    stats_text = f"📊 **{config.MUSIC_BOT_NAME} Statistics**\n\n" \
                 f"**👥 Users & Chats:**\n" \
                 f"**Total Users:** `{global_stats.get('total_users', 0)}`\n" \
                 f"**Total Chats:** `{global_stats.get('total_chats', 0)}`\n" \
                 f"**Active Queues:** `{queue_stats['total_chats']}`\n\n" \
                 f"**🎵 Music Stats:**\n" \
                 f"**Songs Played:** `{global_stats.get('total_songs_played', 0)}`\n" \
                 f"**Songs in Queue:** `{queue_stats['total_songs']}`\n" \
                 f"**Active Loops:** `{queue_stats['active_loops']}`\n" \
                 f"**Currently Playing:** `{'Yes' if bot.is_playing else 'No'}`\n\n" \
                 f"**💾 System Resources:**\n" \
                 f"**Memory Usage:** `{memory.percent}%`\n" \
                 f"**Disk Usage:** `{disk.percent}%`\n" \
                 f"**Platform:** `{platform.system()} {platform.release()}`\n\n" \
                 f"**📚 Libraries:**\n" \
                 f"**Pyrogram:** `{pyrogram.__version__}`\n" \
                 f"**PyTgCalls:** `{pytgcalls.__version__}`\n" \
                 f"**Python:** `{platform.python_version()}`"
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 Refresh", callback_data="refresh_stats"),
            InlineKeyboardButton("📈 Details", callback_data="detailed_stats")
        ]
    ])
    
    await message.reply_text(stats_text, reply_markup=keyboard)

async def help_handler(client: Client, message: Message, bot):
    """Handle detailed help command"""
    help_text = config.HELP_TEXT
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎵 Music Commands", callback_data="help_music"),
            InlineKeyboardButton("👮‍♂️ Admin Commands", callback_data="help_admin")
        ],
        [
            InlineKeyboardButton("📊 Info Commands", callback_data="help_info"),
            InlineKeyboardButton("🔧 Settings", callback_data="help_settings")
        ],
        [
            InlineKeyboardButton("❓ FAQ", callback_data="help_faq"),
            InlineKeyboardButton("📞 Support", url="https://t.me/your_support_group")
        ]
    ])
    
    await message.reply_text(help_text, reply_markup=keyboard)

async def about_handler(client: Client, message: Message, bot):
    """Handle /about command"""
    about_text = f"ℹ️ **About {config.MUSIC_BOT_NAME}**\n\n" \
                 f"**Version:** `{config.__version__}`\n" \
                 f"**Developer:** [Your Name](https://t.me/your_username)\n" \
                 f"**Repository:** [GitHub](https://github.com/YourUsername/VCPlayMusicBot)\n" \
                 f"**Language:** Python 3.11\n\n" \
                 f"**🛠 Built With:**\n" \
                 f"• [Pyrogram](https://github.com/pyrogram/pyrogram) - MTProto API Client\n" \
                 f"• [PyTgCalls](https://github.com/pytgcalls/pytgcalls) - Voice Chat Integration\n" \
                 f"• [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Media Downloader\n" \
                 f"• [FFmpeg](https://ffmpeg.org/) - Media Processing\n\n" \
                 f"**📊 Performance:**\n" \
                 f"• High-quality audio streaming up to 320kbps\n" \
                 f"• Video streaming support up to 720p\n" \
                 f"• Advanced queue management\n" \
                 f"• Multi-platform music support\n\n" \
                 f"**💝 Support Development:**\n" \
                 f"If you find this bot useful, please consider:\n" \
                 f"• ⭐ Star the repository\n" \
                 f"• 🐛 Report issues\n" \
                 f"• 🤝 Contribute improvements\n" \
                 f"• 💰 Donate for server costs"
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⭐ Star Repository", url="https://github.com/YourUsername/VCPlayMusicBot"),
            InlineKeyboardButton("🐛 Report Bug", url="https://github.com/YourUsername/VCPlayMusicBot/issues")
        ],
        [
            InlineKeyboardButton("💰 Donate", url="https://paypal.me/yourusername"),
            InlineKeyboardButton("📢 Updates", url="https://t.me/your_channel")
        ]
    ])
    
    await message.reply_text(about_text, reply_markup=keyboard)

async def language_handler(client: Client, message: Message, bot):
    """Handle /language command"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"),
            InlineKeyboardButton("🇮🇳 हिन्दी", callback_data="lang_hi"),
        ],
        [
            InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es"),
            InlineKeyboardButton("🇫🇷 Français", callback_data="lang_fr"),
        ],
        [
            InlineKeyboardButton("🇩🇪 Deutsch", callback_data="lang_de"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        ]
    ])
    
    await message.reply_text(
        "🌐 **Select Language / भाषा चुनें**\n\n"
        "Choose your preferred language for bot responses:",
        reply_markup=keyboard
    )

# Admin command handlers

async def reload_handler(client: Client, message: Message, bot):
    """Handle /reload command (Admin only)"""
    if message.from_user.id not in config.ADMINS:
        return await message.reply_text("❌ **You don't have permission to use this command!**")
    
    reload_msg = await message.reply_text("🔄 **Reloading bot configuration...**")
    
    try:
        # Reload config module
        import importlib
        import config as config_module
        importlib.reload(config_module)
        
        # Update bot configuration
        # Note: Some changes might require full restart
        
        await reload_msg.edit_text(
            "✅ **Bot configuration reloaded successfully!**\n\n"
            "**Note:** Some changes might require a full restart to take effect."
        )
    except Exception as e:
        await reload_msg.edit_text(f"❌ **Reload failed:** `{str(e)}`")

async def logs_handler(client: Client, message: Message, bot):
    """Handle /logs command (Admin only)"""
    if message.from_user.id not in config.ADMINS:
        return await message.reply_text("❌ **You don't have permission to use this command!**")
    
    try:
        # Read last 50 lines from log file
        with open('musicbot.log', 'r') as log_file:
            lines = log_file.readlines()
            recent_logs = ''.join(lines[-50:])
        
        if len(recent_logs) > 4000:
            # Send as file if too long
            await message.reply_document('musicbot.log', caption="📋 **Bot Logs**")
        else:
            await message.reply_text(f"📋 **Recent Bot Logs:**\n\n``````")
    
    except FileNotFoundError:
        await message.reply_text("❌ **Log file not found!**")
    except Exception as e:
        await message.reply_text(f"❌ **Error reading logs:** `{str(e)}`")

async def speedtest_handler(client: Client, message: Message, bot):
    """Handle /speedtest command (Admin only)"""
    if message.from_user.id not in config.ADMINS:
        return await message.reply_text("❌ **You don't have permission to use this command!**")
    
    test_msg = await message.reply_text("🚀 **Running speed test... This may take a moment.**")
    
    try:
        import speedtest
        
        # Create speedtest instance
        st = speedtest.Speedtest()
        
        # Get best servers
        await test_msg.edit_text("🔍 **Finding best servers...**")
        st.get_best_server()
        
        # Test download speed
        await test_msg.edit_text("⬇️ **Testing download speed...**")
        download_speed = st.download() / 1024 / 1024  # Convert to Mbps
        
        # Test upload speed
        await test_msg.edit_text("⬆️ **Testing upload speed...**")
        upload_speed = st.upload() / 1024 / 1024  # Convert to Mbps
        
        # Get ping
        ping = st.results.ping
        
        # Get server info
        server = st.get_best_server()
        
        result_text = f"🚀 **Server Speed Test Results**\n\n" \
                     f"**📡 Server:** {server['name']} ({server['country']})\n" \
                     f"**📍 Location:** {server['name']}, {server['country']}\n" \
                     f"**🏷 ISP:** {server['sponsor']}\n\n" \
                     f"**⬇️ Download:** `{download_speed:.2f} Mbps`\n" \
                     f"**⬆️ Upload:** `{upload_speed:.2f} Mbps`\n" \
                     f"**🏓 Ping:** `{ping:.2f} ms`\n\n" \
                     f"**📊 Results URL:** {st.results.share()}"
        
        await test_msg.edit_text(result_text)
    
    except ImportError:
        await test_msg.edit_text("❌ **Speedtest library not installed!**")
    except Exception as e:
        await test_msg.edit_text(f"❌ **Speed test failed:** `{str(e)}`")

async def broadcast_handler(client: Client, message: Message, bot):
    """Handle /broadcast command (Admin only)"""
    if message.from_user.id not in config.ADMINS:
        return await message.reply_text("❌ **You don't have permission to use this command!**")
    
    if not message.reply_to_message:
        return await message.reply_text(
            "❌ **Usage:** Reply to a message with `/broadcast`\n\n"
            "The replied message will be sent to all chats using the bot."
        )
    
    broadcast_msg = await message.reply_text("📢 **Starting broadcast...**")
    
    try:
        # Get all chats from database or queue manager
        success_count = 0
        failed_count = 0
        
        # Get active chats from queue manager
        active_chats = list(bot.queue_manager.queues.keys())
        
        for chat_id in active_chats:
            try:
                await client.copy_message(
                    chat_id=chat_id,
                    from_chat_id=message.chat.id,
                    message_id=message.reply_to_message.message_id
                )
                success_count += 1
                await asyncio.sleep(0.1)  # Rate limiting
            except Exception:
                failed_count += 1
        
        await broadcast_msg.edit_text(
            f"📢 **Broadcast Complete!**\n\n"
            f"**✅ Successful:** `{success_count}`\n"
            f"**❌ Failed:** `{failed_count}`\n"
            f"**📊 Total:** `{success_count + failed_count}`"
        )
    
    except Exception as e:
        await broadcast_msg.edit_text(f"❌ **Broadcast failed:** `{str(e)}`")

async def ban_user_handler(client: Client, message: Message, bot):
    """Handle /ban command (Admin only)"""
    if message.from_user.id not in config.ADMINS:
        return await message.reply_text("❌ **You don't have permission to use this command!**")
    
    if len(message.command) != 2:
        return await message.reply_text(
            "❌ **Usage:** `/ban [user_id]`\n\n"
            "**Example:** `/ban 12345678`"
        )
    
    try:
        user_id = int(message.command[1])
        
        # Ban user in database
        await bot.db.ban_user(user_id)
        
        await message.reply_text(
            f"🚫 **User banned successfully!**\n\n"
            f"**User ID:** `{user_id}`"
        )
    
    except ValueError:
        await message.reply_text("❌ **Invalid user ID!**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** `{str(e)}`")

async def unban_user_handler(client: Client, message: Message, bot):
    """Handle /unban command (Admin only)"""
    if message.from_user.id not in config.ADMINS:
        return await message.reply_text("❌ **You don't have permission to use this command!**")
    
    if len(message.command) != 2:
        return await message.reply_text(
            "❌ **Usage:** `/unban [user_id]`\n\n"
            "**Example:** `/unban 12345678`"
        )
    
    try:
        user_id = int(message.command[1])
        
        # Check if user is banned
        if not await bot.db.is_user_banned(user_id):
            return await message.reply_text("❌ **User is not banned!**")
        
        # Unban user
        await bot.db.unban_user(user_id)
        
        await message.reply_text(
            f"✅ **User unbanned successfully!**\n\n"
            f"**User ID:** `{user_id}`"
        )
    
    except ValueError:
        await message.reply_text("❌ **Invalid user ID!**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** `{str(e)}`")

async def maintenance_handler(client: Client, message: Message, bot):
    """Handle /maintenance command (Owner only)"""
    if message.from_user.id != config.OWNER_ID:
        return await message.reply_text("❌ **Only the bot owner can use this command!**")
    
    maintenance_msg = await message.reply_text("🔧 **Starting maintenance tasks...**")
    
    try:
        # Cleanup downloads
        await bot.downloader.cleanup_downloads()
        await maintenance_msg.edit_text("🔧 **Cleaning up downloads...**")
        
        # Cleanup database
        await bot.db.cleanup_old_data()
        await maintenance_msg.edit_text("🔧 **Cleaning up database...**")
        
        # Clear inactive queues
        # Add more maintenance tasks as needed
        
        await maintenance_msg.edit_text(
            "✅ **Maintenance completed successfully!**\n\n"
            "**Tasks completed:**\n"
            "• Cleaned up old downloads\n"
            "• Cleaned up database records\n"
            "• Optimized performance"
        )
    
    except Exception as e:
        await maintenance_msg.edit_text(f"❌ **Maintenance failed:** `{str(e)}`")

async def system_info_handler(client: Client, message: Message, bot):
    """Handle /sysinfo command (Admin only)"""
    if message.from_user.id not in config.ADMINS:
        return await message.reply_text("❌ **You don't have permission to use this command!**")
    
    try:
        # System information
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        boot_time = psutil.boot_time()
        
        system_text = f"🖥 **System Information**\n\n" \
                     f"**💻 Hardware:**\n" \
                     f"**CPU Cores:** `{cpu_count}`\n" \
                     f"**CPU Frequency:** `{cpu_freq.max:.2f} MHz`\n" \
                     f"**Total Memory:** `{humanbytes(memory.total)}`\n" \
                     f"**Total Disk:** `{humanbytes(disk.total)}`\n\n" \
                     f"**📊 Current Usage:**\n" \
                     f"**CPU Usage:** `{psutil.cpu_percent()}%`\n" \
                     f"**Memory Used:** `{humanbytes(memory.used)} ({memory.percent}%)`\n" \
                     f"**Disk Used:** `{humanbytes(disk.used)} ({disk.percent}%)`\n\n" \
                     f"**🕐 Uptime:**\n" \
                     f"**System:** `{get_readable_time(time.time() - boot_time)}`\n" \
                     f"**Bot:** `{get_readable_time(time.time() - getattr(bot, 'start_time', time.time()))}`\n\n" \
                     f"**🐍 Software:**\n" \
                     f"**OS:** `{platform.system()} {platform.release()}`\n" \
                     f"**Python:** `{platform.python_version()}`\n" \
                     f"**Architecture:** `{platform.architecture()[0]}`"
        
        await message.reply_text(system_text)
        
    except Exception as e:
        await message.reply_text(f"❌ **Error getting system info:** `{str(e)}`")
