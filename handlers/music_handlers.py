# Music command handlers for VCPlay Music Bot

import asyncio
import os
import time
from typing import Union
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped, VideoPiped, InputStream
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio, MediumQualityAudio, LowQualityAudio,
    HighQualityVideo, MediumQualityVideo, LowQualityVideo
)
import config
from utils.decorators import authorized_users_only, check_voice_chat
from utils.helpers import get_duration, convert_seconds, get_thumbnail

# All the handler functions from previous music_handlers.py remain the same...
# [Previous music_handlers.py code goes here - no changes needed]

async def play_handler(client: Client, message: Message, bot):
    """Handle /play command for audio streaming"""
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(
            "❌ **Usage:** `/play [song name or YouTube link]`\n"
            "💡 **Tip:** Reply to an audio file to play it!"
        )
    
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Add user to database
    await bot.db.add_user(user_id, message.from_user.username or "", message.from_user.first_name or "")
    
    # Check authorization
    if not await authorized_users_only(client, message, bot):
        return
    
    # Get query
    if message.reply_to_message and message.reply_to_message.audio:
        # Play replied audio file
        audio_file = message.reply_to_message.audio
        title = audio_file.title or audio_file.file_name or "Unknown"
        duration = convert_seconds(audio_file.duration)
        
        # Download the file
        downloading_msg = await message.reply_text("📥 **Downloading audio file...**")
        
        try:
            audio_path = await client.download_media(audio_file)
        except Exception as e:
            await downloading_msg.edit_text(f"❌ **Download failed:** {str(e)}")
            return
        
        song_info = {
            "title": title,
            "duration": duration,
            "thumbnail": config.THUMBNAIL_URL,
            "requested_by": message.from_user.mention,
            "path": audio_path,
            "type": "file"
        }
        
    else:
        # Search and download from YouTube
        query = " ".join(message.command[1:])
        
        searching_msg = await message.reply_text(f"🔍 **Searching:** `{query}`")
        
        try:
            # Search for the song
            search_results = await bot.downloader.search_youtube(query)
            if not search_results:
                await searching_msg.edit_text("❌ **No results found!**")
                return
            
            # Get the first result
            video_info = search_results[0]
            
            # Check duration limit
            if video_info['duration'] > config.MAX_DURATION_LIMIT:
                await searching_msg.edit_text(
                    f"❌ **Duration limit exceeded!**\n"
                    f"**Max allowed:** {convert_seconds(config.MAX_DURATION_LIMIT)}\n"
                    f"**Video duration:** {convert_seconds(video_info['duration'])}"
                )
                return
            
            await searching_msg.edit_text("📥 **Downloading audio...**")
            
            # Download audio
            audio_path = await bot.downloader.download_audio(video_info['url'])
            if not audio_path:
                await searching_msg.edit_text("❌ **Download failed!**")
                return
            
            song_info = {
                "title": video_info['title'],
                "duration": convert_seconds(video_info['duration']),
                "thumbnail": video_info['thumbnail'],
                "requested_by": message.from_user.mention,
                "path": audio_path,
                "type": "youtube",
                "url": video_info['url']
            }
            
        except Exception as e:
            await searching_msg.edit_text(f"❌ **Error:** {str(e)}")
            return
    
    # Check if already connected to voice chat
    try:
        if not bot.call_py.get_call(chat_id):
            await bot.call_py.join_group_call(
                chat_id,
                InputStream(
                    AudioPiped(
                        song_info['path'],
                        HighQualityAudio() if config.AUDIO_QUALITY == "high" else
                        MediumQualityAudio() if config.AUDIO_QUALITY == "medium" else
                        LowQualityAudio()
                    )
                ),
                stream_type=StreamType().local_stream
            )
        else:
            await bot.call_py.change_stream(
                chat_id,
                InputStream(
                    AudioPiped(
                        song_info['path'],
                        HighQualityAudio() if config.AUDIO_QUALITY == "high" else MediumQualityAudio()
                    )
                )
            )
    except Exception as e:
        await message.reply_text(f"❌ **Failed to join/change stream:** {str(e)}")
        return
    
    # Add to queue or start playing
    if bot.queue_manager.is_empty(chat_id) and not bot.is_playing:
        # Start playing immediately
        bot.is_playing = True
        bot.current_chat = chat_id
        
        # Send now playing message
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⏸ Pause", callback_data=f"pause_{chat_id}"),
                InlineKeyboardButton("⏭ Skip", callback_data=f"skip_{chat_id}"),
                InlineKeyboardButton("⏹ Stop", callback_data=f"stop_{chat_id}")
            ],
            [
                InlineKeyboardButton("📜 Queue", callback_data=f"queue_{chat_id}"),
                InlineKeyboardButton("🔄 Loop", callback_data=f"loop_{chat_id}")
            ]
        ])
        
        try:
            await message.reply_photo(
                song_info['thumbnail'],
                caption=f"🎵 **Now Playing**\n\n"
                       f"**Title:** {song_info['title']}\n"
                       f"**Duration:** {song_info['duration']}\n"
                       f"**Requested by:** {song_info['requested_by']}\n"
                       f"**Chat:** {message.chat.title}",
                reply_markup=keyboard
            )
        except Exception:
            await message.reply_text(
                f"🎵 **Now Playing**\n\n"
                f"**Title:** {song_info['title']}\n"
                f"**Duration:** {song_info['duration']}\n"
                f"**Requested by:** {song_info['requested_by']}\n"
                f"**Chat:** {message.chat.title}",
                reply_markup=keyboard
            )
        
    else:
        # Add to queue
        position = bot.queue_manager.add_to_queue(chat_id, song_info)
        
        await message.reply_text(
            f"✅ **Added to queue at position #{position}**\n\n"
            f"**Title:** {song_info['title']}\n"
            f"**Duration:** {song_info['duration']}\n"
            f"**Requested by:** {song_info['requested_by']}"
        )
    
    # Clean up the processing message
    try:
        if 'searching_msg' in locals():
            await searching_msg.delete()
        if 'downloading_msg' in locals():
            await downloading_msg.delete()
    except:
        pass

# Add all other handler functions from the original music_handlers.py...
# [Rest of the handlers remain the same]
