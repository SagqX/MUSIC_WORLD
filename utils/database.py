# Database utilities for VCPlay Music Bot

import motor.motor_asyncio
from typing import Dict, List, Optional, Any
import config
from datetime import datetime, timedelta

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
                
                # Create indexes
                await self._create_indexes()
                
            except Exception as e:
                print(f"❌ Failed to connect to MongoDB: {e}")
                self.connected = False
        else:
            print("⚠️ No MongoDB URI provided, running without database")
    
    async def disconnect(self):
        """Disconnect from database"""
        if self.client and self.connected:
            self.client.close()
            self.connected = False
            print("📤 Disconnected from MongoDB")
    
    async def _create_indexes(self):
        """Create database indexes for better performance"""
        try:
            # User indexes
            await self.users.create_index("user_id", unique=True)
            
            # Chat indexes
            await self.chats.create_index("chat_id", unique=True)
            
            # Stats indexes
            await self.stats.create_index([("chat_id", 1), ("date", -1)])
            
            # Playlist indexes
            await self.playlists.create_index([("user_id", 1), ("name", 1)])
            
        except Exception as e:
            print(f"Error creating indexes: {e}")
    
    # User management
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
    
    async def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user data"""
        if not self.connected:
            return None
        
        try:
            return await self.users.find_one({"user_id": user_id})
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    async def ban_user(self, user_id: int):
        """Ban user"""
        if not self.connected:
            return
        
        try:
            await self.users.update_one(
                {"user_id": user_id},
                {"$set": {"is_banned": True, "ban_date": datetime.utcnow()}},
                upsert=True
            )
        except Exception as e:
            print(f"Error banning user: {e}")
    
    async def unban_user(self, user_id: int):
        """Unban user"""
        if not self.connected:
            return
        
        try:
            await self.users.update_one(
                {"user_id": user_id},
                {"$set": {"is_banned": False}, "$unset": {"ban_date": 1}}
            )
        except Exception as e:
            print(f"Error unbanning user: {e}")
    
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
    
    # Chat management
    async def add_chat(self, chat_id: int, chat_title: str = "", chat_type: str = ""):
        """Add or update chat in database"""
        if not self.connected:
            return
        
        try:
            chat_data = {
                "chat_id": chat_id,
                "chat_title": chat_title,
                "chat_type": chat_type,
                "join_date": datetime.utcnow(),
                "last_active": datetime.utcnow(),
                "settings": {
                    "language": config.DEFAULT_LANGUAGE,
                    "admin_only": False,
                    "delete_messages": True,
                    "welcome_message": True
                },
                "stats": {
                    "songs_played": 0,
                    "commands_used": 0,
                    "total_duration": 0
                }
            }
            
            await self.chats.update_one(
                {"chat_id": chat_id},
                {"$setOnInsert": chat_data, "$set": {"last_active": datetime.utcnow()}},
                upsert=True
            )
        except Exception as e:
            print(f"Error adding chat: {e}")
    
    async def get_chat(self, chat_id: int) -> Optional[Dict]:
        """Get chat data"""
        if not self.connected:
            return None
        
        try:
            return await self.chats.find_one({"chat_id": chat_id})
        except Exception as e:
            print(f"Error getting chat: {e}")
            return None
    
    async def get_global_stats(self) -> Dict[str, Any]:
        """Get global bot statistics"""
        if not self.connected:
            return {"total_users": 0, "total_chats": 0, "total_songs_played": 0}
        
        try:
            # Count total users and chats
            total_users = await self.users.count_documents({})
            total_chats = await self.chats.count_documents({})
            
            # Get total songs played
            pipeline = [
                {"$group": {"_id": None, "total_songs": {"$sum": "$stats.songs_played"}}}
            ]
            result = await self.chats.aggregate(pipeline).to_list(1)
            total_songs = result[0]["total_songs"] if result else 0
            
            return {
                "total_users": total_users,
                "total_chats": total_chats,
                "total_songs_played": total_songs,
            }
        except Exception as e:
            print(f"Error getting global stats: {e}")
            return {"total_users": 0, "total_chats": 0, "total_songs_played": 0}
    
    async def cleanup_old_data(self, days: int = 30):
        """Clean up old data from database"""
        if not self.connected:
            return
        
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Remove old stats
            await self.stats.delete_many({"date": {"$lt": cutoff_date}})
            
            # Remove inactive users
            await self.users.delete_many({
                "last_seen": {"$lt": cutoff_date},
                "commands_used": {"$lt": 5}
            })
            
            print(f"Cleaned up data older than {days} days")
            
        except Exception as e:
            print(f"Error during cleanup: {e}")
