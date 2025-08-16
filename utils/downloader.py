# YouTube downloader utility for VCPlay Music Bot

import asyncio
import os
import re
from typing import List, Dict, Optional
import yt_dlp
import config

class YouTubeDownloader:
    def __init__(self):
        self.ydl_opts = {
            'format': 'best[height<=720]/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': f'{config.DOWNLOAD_DIR}/%(title)s.%(ext)s',
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'writethumbnail': False,
            'writeinfojson': False,
        }
        
        self.audio_opts = {
            **self.ydl_opts,
            'format': 'bestaudio[ext=m4a]/bestaudio',
            'extractaudio': True,
            'audioformat': 'mp3',
            'audioquality': '192K',
        }
        
        self.video_opts = {
            **self.ydl_opts,
            'format': 'best[height<=720]/best',
            'extractaudio': False,
        }
    
    async def search_youtube(self, query: str, video: bool = False, limit: int = 1) -> List[Dict]:
        """Search YouTube for videos/audio"""
        try:
            search_query = f"ytsearch{limit}:{query}"
            
            ydl_opts = self.video_opts if video else self.audio_opts
            ydl_opts['quiet'] = True
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                search_results = await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: ydl.extract_info(search_query, download=False)
                )
            
            if not search_results or 'entries' not in search_results:
                return []
            
            results = []
            for entry in search_results['entries'][:limit]:
                if entry:
                    result = {
                        'title': entry.get('title', 'Unknown'),
                        'duration': entry.get('duration', 0),
                        'url': entry.get('webpage_url', ''),
                        'thumbnail': self._get_best_thumbnail(entry.get('thumbnails', [])),
                        'uploader': entry.get('uploader', 'Unknown'),
                        'view_count': entry.get('view_count', 0),
                        'id': entry.get('id', ''),
                    }
                    results.append(result)
            
            return results
        
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def _get_best_thumbnail(self, thumbnails: List[Dict]) -> str:
        """Get the best quality thumbnail URL"""
        if not thumbnails:
            return config.THUMBNAIL_URL
        
        # Sort by width (descending)
        sorted_thumbs = sorted(
            thumbnails, 
            key=lambda x: x.get('width', 0), 
            reverse=True
        )
        
        return sorted_thumbs[0].get('url', config.THUMBNAIL_URL)
    
    async def download_audio(self, url: str) -> Optional[str]:
        """Download audio from YouTube URL"""
        try:
            filename = None
            
            def progress_hook(d):
                nonlocal filename
                if d['status'] == 'finished':
                    filename = d['filename']
            
            self.audio_opts['progress_hooks'] = [progress_hook]
            
            with yt_dlp.YoutubeDL(self.audio_opts) as ydl:
                await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: ydl.download([url])
                )
            
            return filename
        
        except Exception as e:
            print(f"Audio download error: {e}")
            return None
    
    async def download_video(self, url: str) -> Optional[str]:
        """Download video from YouTube URL"""
        try:
            filename = None
            
            def progress_hook(d):
                nonlocal filename
                if d['status'] == 'finished':
                    filename = d['filename']
            
            self.video_opts['progress_hooks'] = [progress_hook]
            
            with yt_dlp.YoutubeDL(self.video_opts) as ydl:
                await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: ydl.download([url])
                )
            
            return filename
        
        except Exception as e:
            print(f"Video download error: {e}")
            return None
    
    async def get_playlist(self, url: str) -> Optional[Dict]:
        """Get playlist information and entries"""
        try:
            playlist_opts = {
                **self.ydl_opts,
                'extract_flat': True,
                'dump_single_json': True,
            }
            
            with yt_dlp.YoutubeDL(playlist_opts) as ydl:
                playlist_info = await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: ydl.extract_info(url, download=False)
                )
            
            if playlist_info and 'entries' in playlist_info:
                entries = []
                for entry in playlist_info['entries'][:config.PLAYLIST_LIMIT]:
                    if entry:
                        entries.append({
                            'title': entry.get('title', 'Unknown'),
                            'duration': entry.get('duration', 0),
                            'webpage_url': entry.get('url', ''),
                            'thumbnail': config.THUMBNAIL_URL
                        })
                
                return {
                    'title': playlist_info.get('title', 'Unknown Playlist'),
                    'uploader': playlist_info.get('uploader', 'Unknown'),
                    'entries': entries,
                    'entry_count': len(entries)
                }
            
            return None
        
        except Exception as e:
            print(f"Playlist extraction error: {e}")
            return None
    
    def is_youtube_url(self, url: str) -> bool:
        """Check if URL is a valid YouTube URL"""
        youtube_regex = re.compile(
            r'^(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )
        return bool(youtube_regex.match(url))
    
    async def cleanup_downloads(self):
        """Clean up old downloaded files"""
        try:
            if not os.path.exists(config.DOWNLOAD_DIR):
                return
            
            import time
            current_time = time.time()
            
            for filename in os.listdir(config.DOWNLOAD_DIR):
                file_path = os.path.join(config.DOWNLOAD_DIR, filename)
                
                if os.path.isfile(file_path):
                    # Delete files older than cleanup interval
                    file_age = current_time - os.path.getctime(file_path)
                    
                    if file_age > config.CLEANUP_INTERVAL:
                        os.remove(file_path)
                        print(f"Cleaned up: {filename}")
        
        except Exception as e:
            print(f"Cleanup error: {e}")
