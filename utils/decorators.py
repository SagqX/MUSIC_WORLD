# Lightweight wrappers split out from helpers where needed

import functools
from pyrogram import Client
from pyrogram.types import Message
import config

def admin_only(func):
    @functools.wraps(func)
    async def wrapper(client: Client, message: Message, bot, *args, **kwargs):
        if message.from_user.id not in config.ADMINS:
            await message.reply_text("❌ **You don't have permission to use this command!**")
            return False
        return await func(client, message, bot, *args, **kwargs)
    return wrapper

async def _is_group_admin(client: Client, chat_id: int, user_id: int) -> bool:
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in ("creator", "administrator")
    except Exception:
        return False

def authorized_users_only(func):
    @functools.wraps(func)
    async def wrapper(client: Client, message: Message, bot, *args, **kwargs):
        # Add user to database
        await bot.db.add_user(
            message.from_user.id,
            message.from_user.username or "",
            message.from_user.first_name or ""
        )
        
        # Check if user is banned
        if await bot.db.is_user_banned(message.from_user.id):
            await message.reply_text("🚫 **You are banned from using this bot!**")
            return False
        
        # If chat is configured admin-only, require group admin
        chat_id = message.chat.id
        is_admin_only = False
        try:
            chat_doc = await bot.db.get_chat(chat_id)
            is_admin_only = bool(chat_doc and chat_doc.get("settings", {}).get("admin_only"))
        except Exception:
            pass
            
        if is_admin_only:
            if not await _is_group_admin(client, chat_id, message.from_user.id):
                await message.reply_text("🔒 **This command is admin-only in this chat.**")
                return False
                
        return await func(client, message, bot, *args, **kwargs)
    return wrapper

def check_voice_chat(func):
    @functools.wraps(func)
    async def wrapper(client: Client, message: Message, bot, *args, **kwargs):
        # Soft-check before trying join; if not running, the join will raise and be handled.
        return await func(client, message, bot, *args, **kwargs)
    return wrapper
