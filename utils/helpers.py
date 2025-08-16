# Helper utilities and decorators for VCPlay Music Bot

import functools
import time
import os
from typing import List, Optional, Union
from pyrogram import Client
from pyrogram.types import Message
import config

def get_readable_time(seconds: int) -> str:
    """Convert seconds to readable time format"""
    if seconds <= 0:
        return "0s"
    
    count = 0
    readable_time = ""
    time_list = []
    time_suffix = ["s", "m", "h", "days"]
    
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
            
        if seconds == 0 and remainder == 0:
            break
            
        time_list.append(int(result))
        seconds = int(remainder)
    
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix[i]
    
    if len(time_list) == 4:
        readable_time += f"{time_list[-1]}, "
    if len(time_list) >= 3:
        readable_time += f"{time_list[-2]}, "
    if len(time_list) >= 2:
        readable_time += f"{time_list[-1]} "
    if time_list:
        readable_time += time_list[0]
    
    return readable_time or "0s"

def convert_seconds(duration: int) -> str:
    """Convert seconds to MM:SS or HH:MM:SS format"""
    if duration == 0:
        return "Unknown"
    
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = duration % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def humanbytes(size: Union[int, float]) -> str:
    """Convert bytes to human readable format"""
    if not size:
        return "0 B"
    
    power = 2**10
    number = 0
    dict_power_n = {0: " ", 1: "K", 2: "M", 3: "G", 4: "T"}
    
    while size > power:
        size /= power
        number += 1
    
    return f"{size:.2f} {dict_power_n[number]}B"

async def get_thumbnail(thumbnails: List) -> str:
    """Get best quality thumbnail from list"""
    if not thumbnails:
        return config.THUMBNAIL_URL
    
    return thumbnails[0].file_id if thumbnails else config.THUMBNAIL_URL

def get_duration(file_path: str) -> int:
    """Get duration of audio/video file"""
    try:
        import subprocess
        result = subprocess.run([
            'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', file_path
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            return int(float(result.stdout.strip()))
    except Exception:
        pass
    return 0

def clean_filename(filename: str) -> str:
    """Clean filename for safe saving"""
    import re
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove multiple spaces and trim
    filename = ' '.join(filename.split())
    # Limit length
    if len(filename) > 200:
        name, ext = os.path.splitext(filename)
        filename = name[:195] + ext
    return filename

async def delete_file(file_path: str):
    """Safely delete a file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")

# Add the authorized_users_only function that was being imported
async def authorized_users_only(client: Client, message: Message, bot) -> bool:
    """Check if user is authorized to use bot"""
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
    
    # Get chat settings
    chat_id = message.chat.id
    try:
        chat_doc = await bot.db.get_chat(chat_id)
        if chat_doc and chat_doc.get("settings", {}).get("admin_only", False):
            # Check if user is admin
            try:
                member = await client.get_chat_member(chat_id, message.from_user.id)
                if member.status not in ["creator", "administrator"]:
                    await message.reply_text("🔒 **This command is restricted to administrators only!**")
                    return False
            except Exception:
                await message.reply_text("❌ **Unable to verify admin status!**")
                return False
    except Exception:
        pass
    
    return True

async def check_voice_chat(client: Client, message: Message, bot) -> bool:
    """Check if voice chat is active (placeholder)"""
    # This is a soft check - the actual voice chat status 
    # will be determined when trying to join
    return True
    