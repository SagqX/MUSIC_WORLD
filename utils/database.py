# Database utilities for VCPlay Music Bot

import motor.motor_asyncio
from typing import Dict, List, Optional, Any
import config
from datetime import datetime

class Database:
    def __init__(self):
        if config.MONGO_DB_URI:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGO_DB_URI)
            self.db = self.client[config.DB_NAME]
            self.users = self.db.users
            self.chats = self.db.chats
            self.stats = self.db.stats
            self.playlists = self.db.playlists
            self.settings = self.db.settings
            self.connected = False
        else:
            self.client = None
            self.connected = False
    
    async def connect(self):
        """Connect to database"""
        if self.client:
            try:
                await self.client.admin.command('ping')
                self.connected = True
                print("✅ Connected to MongoDB successfully")
                
            except Exception as e:
                print(f"❌ Failed to connect to MongoDB: {e}")
                self.connected = False
    
    async def disconnect(self):
        """Disconnect from database"""
        if self.client and self.connected:
            self.client.close()
            self.connected = False
            print("📤 Disconnected from MongoDB")
    
    async def add_user(self, user_id: int, username: str = "", first_name: str = ""):
        """Add or update user in database"""
        if not self.connected:
            return
        
        try:
            user_data = {
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "join_date": datetime.utcnow(),
                "last_seen": datetime.utcnow(),
                "commands_used": 0,
                "is_banned": False
            }
            
            await self.users.update_one(
                {"user_id": user_id},
                {"$setOnInsert": user_data, "$set": {"last_seen": datetime.utcnow()}},
                upsert=True
            )
        except Exception as e:
            print(f"Error adding user: {e}")
    
    async def is_user_banned(self, user_id: int) -> bool:
        """Check if user is banned"""
        if not self.connected:
            return False
        
        try:
            user = await self.users.find_one({"user_id": user_id})
            return user.get("is_banned", False) if user else False
        except Exception as e:
            print(f"Error checking ban status: {e}")
            return False
    
    async def get_global_stats(self) -> Dict[str, Any]:
        """Get global bot statistics"""
        if not self.connected:
            return {"total_users": 0, "total_chats": 0, "total_songs_played": 0}
        
        try:
            total_users = await self.users.count_documents({})
            total_chats = await self.chats.count_documents({})
            
            return {
                "total_users": total_users,
                "total_chats": total_chats,
                "total_songs_played": 0
            }
        except Exception as e:
            print(f"Error getting global stats: {e}")
            return {"total_users": 0, "total_chats": 0, "total_songs_played": 0}
            
