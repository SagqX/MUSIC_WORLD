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

async def play_handler(client: Client, message: Message, bot):
    """Handle /play command for audio streaming"""
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(
            "❌ **Usage:** `/play [song name or YouTube link]`\n"
            "💡 **Tip:** Reply to an audio file to play it!"
        )
    
    chat_id = message.chat.id
    user_id = message.from_user.id
    
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
    if not bot.call_py.get_call(chat_id):
        try:
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
        except Exception as e:
            await message.reply_text(f"❌ **Failed to join voice chat:** {str(e)}")
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
        
        await message.reply_photo(
            song_info['thumbnail'],
            caption=f"🎵 **Now Playing**\n\n"
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

async def vplay_handler(client: Client, message: Message, bot):
    """Handle /vplay command for video streaming"""
    if len(message.command) < 2:
        return await message.reply_text(
            "❌ **Usage:** `/vplay [video name or YouTube link]`"
        )
    
    chat_id = message.chat.id
    query = " ".join(message.command[1:])
    
    searching_msg = await message.reply_text(f"🔍 **Searching video:** `{query}`")
    
    try:
        # Search for video
        search_results = await bot.downloader.search_youtube(query, video=True)
        if not search_results:
            await searching_msg.edit_text("❌ **No video results found!**")
            return
        
        video_info = search_results[0]
        
        # Check duration limit
        if video_info['duration'] > config.MAX_DURATION_LIMIT:
            await searching_msg.edit_text(
                f"❌ **Duration limit exceeded!**\n"
                f"**Max allowed:** {convert_seconds(config.MAX_DURATION_LIMIT)}\n"
                f"**Video duration:** {convert_seconds(video_info['duration'])}"
            )
            return
        
        await searching_msg.edit_text("📥 **Downloading video...**")
        
        # Download video
        video_path = await bot.downloader.download_video(video_info['url'])
        if not video_path:
            await searching_msg.edit_text("❌ **Video download failed!**")
            return
        
        song_info = {
            "title": video_info['title'],
            "duration": convert_seconds(video_info['duration']),
            "thumbnail": video_info['thumbnail'],
            "requested_by": message.from_user.mention,
            "path": video_path,
            "type": "video",
            "url": video_info['url']
        }
        
        # Join or change stream
        try:
            if not bot.call_py.get_call(chat_id):
                await bot.call_py.join_group_call(
                    chat_id,
                    InputStream(
                        AudioPiped(video_path, HighQualityAudio()),
                        VideoPiped(
                            video_path,
                            HighQualityVideo() if config.VIDEO_QUALITY == "high" else
                            MediumQualityVideo() if config.VIDEO_QUALITY == "medium" else
                            LowQualityVideo()
                        )
                    ),
                    stream_type=StreamType().local_stream
                )
            else:
                await bot.call_py.change_stream(
                    chat_id,
                    InputStream(
                        AudioPiped(video_path, HighQualityAudio()),
                        VideoPiped(video_path, MediumQualityVideo())
                    )
                )
        except Exception as e:
            await searching_msg.edit_text(f"❌ **Failed to stream video:** {str(e)}")
            return
        
        # Update status
        bot.is_playing = True
        bot.current_chat = chat_id
        
        # Send now playing message
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⏸ Pause", callback_data=f"pause_{chat_id}"),
                InlineKeyboardButton("⏭ Skip", callback_data=f"skip_{chat_id}"),
                InlineKeyboardButton("⏹ Stop", callback_data=f"stop_{chat_id}")
            ]
        ])
        
        await message.reply_photo(
            song_info['thumbnail'],
            caption=f"📹 **Now Playing Video**\n\n"
                   f"**Title:** {song_info['title']}\n"
                   f"**Duration:** {song_info['duration']}\n"
                   f"**Requested by:** {song_info['requested_by']}\n"
                   f"**Chat:** {message.chat.title}",
            reply_markup=keyboard
        )
        
        await searching_msg.delete()
        
    except Exception as e:
        await searching_msg.edit_text(f"❌ **Error:** {str(e)}")

async def pause_handler(client: Client, message: Message, bot):
    """Handle /pause command"""
    chat_id = message.chat.id
    
    if not bot.is_playing:
        return await message.reply_text("❌ **Nothing is currently playing!**")
    
    if bot.is_paused:
        return await message.reply_text("⏸ **Already paused!**")
    
    try:
        await bot.call_py.pause_stream(chat_id)
        bot.is_paused = True
        
        await message.reply_text(
            "⏸ **Paused!**\n\n"
            "💡 Use `/resume` to continue playing."
        )
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

async def resume_handler(client: Client, message: Message, bot):
    """Handle /resume command"""
    chat_id = message.chat.id
    
    if not bot.is_playing:
        return await message.reply_text("❌ **Nothing is currently playing!**")
    
    if not bot.is_paused:
        return await message.reply_text("▶️ **Already playing!**")
    
    try:
        await bot.call_py.resume_stream(chat_id)
        bot.is_paused = False
        
        await message.reply_text(
            "▶️ **Resumed!**\n\n"
            "💡 Use `/pause` to pause again."
        )
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

async def skip_handler(client: Client, message: Message, bot):
    """Handle /skip command"""
    chat_id = message.chat.id
    
    if not bot.is_playing:
        return await message.reply_text("❌ **Nothing is currently playing!**")
    
    # Check if there's anything in queue
    if bot.queue_manager.is_empty(chat_id):
        # Stop current stream
        try:
            await bot.call_py.leave_group_call(chat_id)
            bot.is_playing = False
            bot.is_paused = False
            bot.current_chat = None
            
            await message.reply_text("⏭ **Skipped!** Queue is empty, stopped playing.")
        except Exception as e:
            await message.reply_text(f"❌ **Error:** {str(e)}")
    else:
        # Play next song
        try:
            next_song = bot.queue_manager.get_next(chat_id)
            
            await bot.call_py.change_stream(
                chat_id,
                InputStream(
                    AudioPiped(
                        next_song['path'],
                        HighQualityAudio() if config.AUDIO_QUALITY == "high" else MediumQualityAudio()
                    )
                )
            )
            
            await message.reply_text(
                f"⏭ **Skipped!**\n\n"
                f"🎵 **Now Playing:**\n"
                f"**Title:** {next_song['title']}\n"
                f"**Duration:** {next_song['duration']}\n"
                f"**Requested by:** {next_song['requested_by']}"
            )
        except Exception as e:
            await message.reply_text(f"❌ **Error:** {str(e)}")

async def stop_handler(client: Client, message: Message, bot):
    """Handle /stop command"""
    chat_id = message.chat.id
    
    if not bot.is_playing:
        return await message.reply_text("❌ **Nothing is currently playing!**")
    
    try:
        # Clear queue
        bot.queue_manager.clear_queue(chat_id)
        
        # Leave voice chat
        await bot.call_py.leave_group_call(chat_id)
        
        # Reset status
        bot.is_playing = False
        bot.is_paused = False
        bot.current_chat = None
        
        await message.reply_text(
            "⏹ **Stopped!**\n\n"
            "✅ Left voice chat and cleared queue."
        )
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

async def queue_handler(client: Client, message: Message, bot):
    """Handle /queue command"""
    chat_id = message.chat.id
    
    queue_list = bot.queue_manager.get_queue(chat_id)
    
    if not queue_list and not bot.is_playing:
        return await message.reply_text("📜 **Queue is empty!**")
    
    queue_text = "📜 **Current Queue:**\n\n"
    
    # Add currently playing
    if bot.is_playing and bot.current_chat == chat_id:
        queue_text += f"🎵 **Now Playing:** Sample Song\n\n"
    
    # Add queue items
    if queue_list:
        queue_text += "⏭ **Up Next:**\n"
        for i, song in enumerate(queue_list[:10], 1):  # Show first 10
            queue_text += f"`{i}.` **{song['title']}** - {song['duration']}\n"
            queue_text += f"    **By:** {song['requested_by']}\n"
        
        if len(queue_list) > 10:
            queue_text += f"\n... and **{len(queue_list) - 10}** more songs"
    else:
        queue_text += "⏭ **No songs in queue**"
    
    await message.reply_text(queue_text)

async def shuffle_handler(client: Client, message: Message, bot):
    """Handle /shuffle command"""
    chat_id = message.chat.id
    
    if bot.queue_manager.is_empty(chat_id):
        return await message.reply_text("❌ **Queue is empty!**")
    
    shuffled_count = bot.queue_manager.shuffle_queue(chat_id)
    
    await message.reply_text(
        f"🔀 **Queue Shuffled!**\n\n"
        f"✅ Shuffled **{shuffled_count}** songs in queue."
    )

async def loop_handler(client: Client, message: Message, bot):
    """Handle /loop command"""
    chat_id = message.chat.id
    
    # Toggle loop mode
    loop_enabled = bot.queue_manager.toggle_loop(chat_id)
    
    status = "enabled" if loop_enabled else "disabled"
    emoji = "🔁" if loop_enabled else "❌"
    
    await message.reply_text(f"{emoji} **Loop mode {status}!**")

async def volume_handler(client: Client, message: Message, bot):
    """Handle /volume command"""
    if len(message.command) != 2:
        return await message.reply_text(
            "❌ **Usage:** `/volume [1-100]`\n"
            "💡 **Example:** `/volume 75`"
        )
    
    try:
        volume = int(message.command[1])
        if not 1 <= volume <= 100:
            raise ValueError()
    except ValueError:
        return await message.reply_text("❌ **Volume must be between 1-100!**")
    
    chat_id = message.chat.id
    
    if not bot.is_playing:
        return await message.reply_text("❌ **Nothing is currently playing!**")
    
    await message.reply_text(f"🔊 **Volume set to {volume}%**")

async def playlist_handler(client: Client, message: Message, bot):
    """Handle /playlist command"""
    if len(message.command) != 2:
        return await message.reply_text(
            "❌ **Usage:** `/playlist [YouTube playlist URL]`"
        )
    
    playlist_url = message.command[1]
    chat_id = message.chat.id
    
    processing_msg = await message.reply_text("🔄 **Processing playlist...**")
    
    try:
        # Extract playlist
        playlist_info = await bot.downloader.get_playlist(playlist_url)
        
        if not playlist_info:
            await processing_msg.edit_text("❌ **Invalid playlist URL or playlist is private!**")
            return
        
        videos = playlist_info['entries'][:config.PLAYLIST_LIMIT]  # Limit playlist size
        
        await processing_msg.edit_text(
            f"📋 **Playlist Found:** {playlist_info['title']}\n"
            f"🎵 **Adding {len(videos)} songs to queue...**"
        )
        
        # Add all videos to queue
        added_count = 0
        for video in videos:
            if video and video.get('duration', 0) <= config.MAX_DURATION_LIMIT:
                song_info = {
                    "title": video['title'],
                    "duration": convert_seconds(video['duration']),
                    "thumbnail": video.get('thumbnail', config.THUMBNAIL_URL),
                    "requested_by": message.from_user.mention,
                    "url": video['webpage_url'],
                    "type": "youtube"
                }
                bot.queue_manager.add_to_queue(chat_id, song_info)
                added_count += 1
        
        await processing_msg.edit_text(
            f"✅ **Playlist Added Successfully!**\n\n"
            f"**Playlist:** {playlist_info['title']}\n"
            f"**Added:** {added_count} songs\n"
            f"**Requested by:** {message.from_user.mention}\n\n"
            f"💡 Use `/play` to start playing!"
        )
        
    except Exception as e:
        await processing_msg.edit_text(f"❌ **Error:** {str(e)}")

async def radio_handler(client: Client, message: Message, bot):
    """Handle /radio command"""
    if len(message.command) < 2:
        stations_text = "📻 **Available Radio Stations:**\n\n"
        for name, url in config.RADIO_STATIONS.items():
            stations_text += f"• `/radio {name}`\n"
        stations_text += "\n💡 **Or use:** `/radio [stream URL]`"
        
        return await message.reply_text(stations_text)
    
    station = message.command[1].lower()
    chat_id = message.chat.id
    
    # Get stream URL
    if station in config.RADIO_STATIONS:
        stream_url = config.RADIO_STATIONS[station]
        title = f"{station.title()} Radio"
    else:
        stream_url = " ".join(message.command[1:])
        title = "Live Stream"
    
    try:
        # Join voice chat and start streaming
        if not bot.call_py.get_call(chat_id):
            await bot.call_py.join_group_call(
                chat_id,
                InputStream(
                    AudioPiped(stream_url, HighQualityAudio())
                ),
                stream_type=StreamType().live_stream
            )
        else:
            await bot.call_py.change_stream(
                chat_id,
                InputStream(
                    AudioPiped(stream_url, HighQualityAudio())
                )
            )
        
        bot.is_playing = True
        bot.current_chat = chat_id
        
        await message.reply_text(
            f"📻 **Now Streaming:**\n\n"
            f"**Station:** {title}\n"
            f"**Requested by:** {message.from_user.mention}\n"
            f"**Chat:** {message.chat.title}"
        )
        
    except Exception as e:
        await message.reply_text(f"❌ **Streaming failed:** {str(e)}")

# Event handlers
async def stream_end_handler(client, update, bot):
    """Handle when stream ends"""
    chat_id = update.chat_id
    
    # Check if there's next song in queue
    if not bot.queue_manager.is_empty(chat_id):
        # Play next song
        try:
            next_song = bot.queue_manager.get_next(chat_id)
            
            await bot.call_py.change_stream(
                chat_id,
                InputStream(
                    AudioPiped(next_song['path'], HighQualityAudio())
                )
            )
            
        except Exception:
            # End streaming on error
            await bot.call_py.leave_group_call(chat_id)
            bot.is_playing = False
            bot.current_chat = None
    else:
        # No more songs, end streaming
        await bot.call_py.leave_group_call(chat_id)
        bot.is_playing = False
        bot.current_chat = None

async def closed_vc_handler(client, chat_id, bot):
    """Handle when voice chat is closed"""
    bot.queue_manager.clear_queue(chat_id)
    bot.is_playing = False
    bot.current_chat = None

async def kicked_handler(client, chat_id, bot):
    """Handle when bot is kicked from voice chat"""
    bot.queue_manager.clear_queue(chat_id)
    bot.is_playing = False
    bot.current_chat = None

async def left_handler(client, chat_id, bot):
    """Handle when bot leaves voice chat"""
    bot.queue_manager.clear_queue(chat_id)
    bot.is_playing = False
    bot.current_chat = None
