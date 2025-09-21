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

import asyncpg
from Bluto.config import DATABASE_URL

pool = None

async def init_db():
    """Initialize the database."""
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)
    with open("Bluto/helpers/schema.sql") as f:
        await pool.execute(f.read())

async def ban_user(user_id: int):
    """Ban a user."""
    await pool.execute("INSERT INTO banned_users (user_id) VALUES ($1) ON CONFLICT DO NOTHING", user_id)

async def unban_user(user_id: int):
    """Unban a user."""
    await pool.execute("DELETE FROM banned_users WHERE user_id = $1", user_id)

async def is_user_banned(user_id: int) -> bool:
    """Check if a user is banned."""
    return bool(await pool.fetchval("SELECT EXISTS(SELECT 1 FROM banned_users WHERE user_id = $1)", user_id))

async def enable_song_download(chat_id: int):
    """Enable song download for a chat."""
    await pool.execute(
        "INSERT INTO song_download_settings (chat_id, enabled) VALUES ($1, TRUE) "
        "ON CONFLICT (chat_id) DO UPDATE SET enabled = TRUE",
        chat_id,
    )

async def disable_song_download(chat_id: int):
    """Disable song download for a chat."""
    await pool.execute(
        "INSERT INTO song_download_settings (chat_id, enabled) VALUES ($1, FALSE) "
        "ON CONFLICT (chat_id) DO UPDATE SET enabled = FALSE",
        chat_id,
    )

async def is_song_download_enabled(chat_id: int) -> bool:
    """Check if song download is enabled for a chat."""
    enabled = await pool.fetchval("SELECT enabled FROM song_download_settings WHERE chat_id = $1", chat_id)
    return enabled if enabled is not None else False

async def create_song_request(
    request_id: str, user_id: int, query: str, chat_id: int, message_id: int
):
    """Create a song request."""
    await pool.execute(
        "INSERT INTO song_requests (request_id, user_id, query, chat_id, message_id) "
        "VALUES ($1, $2, $3, $4, $5)",
        request_id,
        user_id,
        query,
        chat_id,
        message_id,
    )

async def get_song_request(request_id: str):
    """Get a song request."""
    return await pool.fetchrow("SELECT * FROM song_requests WHERE request_id = $1", request_id)

async def delete_song_request(request_id: str):
    """Delete a song request."""
    await pool.execute("DELETE FROM song_requests WHERE request_id = $1", request_id)


import json

async def add_to_queue(chat_id: int, song_details: dict, at_front: bool = False):
    """Add a song to the queue."""
    if at_front:
        await pool.execute(
            "UPDATE queue SET position = position + 1 WHERE chat_id = $1; "
            "INSERT INTO queue (chat_id, song_details, position) VALUES ($1, $2, 1)",
            chat_id,
            json.dumps(song_details),
        )
    else:
        max_pos = await pool.fetchval("SELECT MAX(position) FROM queue WHERE chat_id = $1", chat_id)
        position = (max_pos or 0) + 1
        await pool.execute(
            "INSERT INTO queue (chat_id, song_details, position) VALUES ($1, $2, $3)",
            chat_id,
            json.dumps(song_details),
            position,
        )


async def get_queue(chat_id: int):
    """Get the queue for a chat."""
    return await pool.fetch("SELECT * FROM queue WHERE chat_id = $1 ORDER BY position", chat_id)


async def get_next_song(chat_id: int):
    """Get the next song from the queue."""
    song = await pool.fetchrow("SELECT * FROM queue WHERE chat_id = $1 ORDER BY position LIMIT 1", chat_id)
    if song:
        await remove_from_queue(song["id"])
    return song


async def clear_queue(chat_id: int):
    """Clear the queue for a chat."""
    await pool.execute("DELETE FROM queue WHERE chat_id = $1", chat_id)


async def shuffle_queue(chat_id: int):
    """Shuffle the queue for a chat."""
    queue = await get_queue(chat_id)
    import random
    random.shuffle(queue)
    await clear_queue(chat_id)
    for i, song in enumerate(queue):
        await pool.execute(
            "INSERT INTO queue (chat_id, song_details, position) VALUES ($1, $2, $3)",
            chat_id,
            song["song_details"],
            i + 1,
        )

async def remove_from_queue(song_id: int):
    """Remove a song from the queue."""
    await pool.execute("DELETE FROM queue WHERE id = $1", song_id)
