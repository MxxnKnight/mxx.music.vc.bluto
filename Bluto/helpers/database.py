# Bluto Music Bot
# https://github.com/mxx-x/Bluto
#
# Copyright (C) 2024-2025 Mxx-x
#
# This file is a part of < https://github.com/mxx-x/Bluto >
# Please read the GNU General Public License v3.0
#
# Thanks To The Source Code Of Yukki Music Bot
# < https://github.com/TeamYukki/YukkiMusicBot >
#
# Thanks To The Source Code Of TgCalls
# < https://github.com/pytgcalls/pytgcalls >
#
#
# This file is part of a project Bluto, a Telegram VC Music Bot.
#
# Bluto is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Bluto is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Bluto. If not, see <https://www.gnu.org/licenses/>.

import motor.motor_asyncio
from Bluto.config import MONGO_DB_URI

# Initialize database client
db_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI)
db = db_client["BlutoBot"]

# Collections
banned_users_collection = db["banned_users"]
song_download_collection = db["song_download"]
song_requests_collection = db["song_requests"]

async def ban_user(user_id: int):
    """Ban a user."""
    await banned_users_collection.insert_one({"user_id": user_id})

async def unban_user(user_id: int):
    """Unban a user."""
    await banned_users_collection.delete_one({"user_id": user_id})

async def is_user_banned(user_id: int) -> bool:
    """Check if a user is banned."""
    return bool(await banned_users_collection.find_one({"user_id": user_id}))

async def enable_song_download(chat_id: int):
    """Enable song download for a chat."""
    await song_download_collection.update_one(
        {"chat_id": chat_id}, {"$set": {"enabled": True}}, upsert=True
    )

async def disable_song_download(chat_id: int):
    """Disable song download for a chat."""
    await song_download_collection.update_one(
        {"chat_id": chat_id}, {"$set": {"enabled": False}}, upsert=True
    )

async def is_song_download_enabled(chat_id: int) -> bool:
    """Check if song download is enabled for a chat."""
    chat = await song_download_collection.find_one({"chat_id": chat_id})
    return chat.get("enabled", False)

async def create_song_request(
    request_id: str, user_id: int, query: str, chat_id: int, message_id: int
):
    """Create a song request."""
    await song_requests_collection.insert_one(
        {
            "request_id": request_id,
            "user_id": user_id,
            "query": query,
            "chat_id": chat_id,
            "message_id": message_id,
        }
    )

async def get_song_request(request_id: str):
    """Get a song request."""
    return await song_requests_collection.find_one({"request_id": request_id})

async def delete_song_request(request_id: str):
    """Delete a song request."""
    await song_requests_collection.delete_one({"request_id": request_id})
