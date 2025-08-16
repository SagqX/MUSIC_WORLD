# Admin-only handlers kept separate for clarity

import importlib
import os
import time
import psutil
import platform
from pyrogram import Client
from pyrogram.types import Message
import config

async def reload_handler(client: Client, message: Message, bot):
    if message.from_user.id not in config.ADMINS:
        return await message.reply_text("❌ You don't have permission to use this.")
    try:
        import config as cfg
        importlib.reload(cfg)
        await message.reply_text("✅ Configuration reloaded (some changes may require restart).")
    except Exception as e:
        await message.reply_text(f"❌ Reload failed: `{e}`")

async def logs_handler(client: Client, message: Message, bot):
    if message.from_user.id not in config.ADMINS:
        return await message.reply_text("❌ You don't have permission to use this.")
    try:
        if os.path.exists("musicbot.log"):
            await message.reply_document("musicbot.log", caption="📋 Bot logs")
        else:
            await message.reply_text("⚠️ Log file not found yet.")
    except Exception as e:
        await message.reply_text(f"❌ Failed to send logs: `{e}`")

async def speedtest_handler(client: Client, message: Message, bot):
    if message.from_user.id not in config.ADMINS:
        return await message.reply_text("❌ You don't have permission to use this.")
    try:
        await message.reply_text("🚀 Running speed test, please wait...")
        import speedtest
        st = speedtest.Speedtest()
        st.get_servers()
        st.get_best_server()
        dl = st.download() / 1024 / 1024
        ul = st.upload() / 1024 / 1024
        ping = st.results.ping
        await message.reply_text(
            "🚀 Speedtest Results\n\n"
            f"⬇️ Download: `{dl:.2f} Mbps`\n"
            f"⬆️ Upload: `{ul:.2f} Mbps`\n"
            f"🏓 Ping: `{ping:.2f} ms`"
        )
    except Exception as e:
        await message.reply_text(f"❌ Speedtest failed: `{e}`")
        