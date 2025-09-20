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

async def ban_user(user_id: int):
    """Ban a user."""
    await banned_users_collection.insert_one({"user_id": user_id})

async def unban_user(user_id: int):
    """Unban a user."""
    await banned_users_collection.delete_one({"user_id": user_id})

async def is_user_banned(user_id: int) -> bool:
    """Check if a user is banned."""
    return bool(await banned_users_collection.find_one({"user_id": user_id}))
