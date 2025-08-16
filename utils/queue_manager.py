# Queue Manager for VCPlay Music Bot

import random
from typing import Dict, List, Optional, Any
from collections import defaultdict

class QueueManager:
    def __init__(self):
        self.queues: Dict[int, List[Dict]] = defaultdict(list)
        self.loop_mode: Dict[int, bool] = defaultdict(bool)
        self.current_playing: Dict[int, Optional[Dict]] = defaultdict(lambda: None)
        
    def add_to_queue(self, chat_id: int, song_info: Dict) -> int:
        """Add song to queue and return position"""
        self.queues[chat_id].append(song_info)
        return len(self.queues[chat_id])
    
    def get_next(self, chat_id: int) -> Optional[Dict]:
        """Get next song from queue"""
        if not self.queues[chat_id]:
            return None
        
        next_song = self.queues[chat_id].pop(0)
        
        # If loop mode is enabled, add current song back to end
        if self.loop_mode[chat_id] and self.current_playing[chat_id]:
            self.queues[chat_id].append(self.current_playing[chat_id])
        
        self.current_playing[chat_id] = next_song
        return next_song
    
    def get_queue(self, chat_id: int) -> List[Dict]:
        """Get current queue"""
        return self.queues[chat_id].copy()
    
    def is_empty(self, chat_id: int) -> bool:
        """Check if queue is empty"""
        return len(self.queues[chat_id]) == 0
    
    def clear_queue(self, chat_id: int):
        """Clear the queue for a chat"""
        self.queues[chat_id].clear()
        self.current_playing[chat_id] = None
    
    def clear_all(self):
        """Clear all queues"""
        self.queues.clear()
        self.loop_mode.clear()
        self.current_playing.clear()
    
    def shuffle_queue(self, chat_id: int) -> int:
        """Shuffle the queue and return count of shuffled songs"""
        if self.queues[chat_id]:
            random.shuffle(self.queues[chat_id])
            return len(self.queues[chat_id])
        return 0
    
    def toggle_loop(self, chat_id: int) -> bool:
        """Toggle loop mode for a chat"""
        self.loop_mode[chat_id] = not self.loop_mode[chat_id]
        return self.loop_mode[chat_id]
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """Get overall queue statistics"""
        total_chats = len(self.queues)
        total_songs = sum(len(queue) for queue in self.queues.values())
        active_loops = sum(1 for enabled in self.loop_mode.values() if enabled)
        
        return {
            'total_chats': total_chats,
            'total_songs': total_songs,
            'active_loops': active_loops,
            'average_queue_size': total_songs / max(total_chats, 1)
        }
