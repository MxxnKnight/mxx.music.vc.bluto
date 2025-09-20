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

import os
from pyrogram import Client, filters
from pyrogram.types import Message

from Bluto.bot import app
from Bluto.config import LOG_GROUP_ID
from Bluto.helpers.decorators import is_banned, force_subscribe
from Bluto.helpers.youtube import download_song


@app.on_message(filters.command("song"))
@is_banned
@force_subscribe
async def song_command(client: Client, message: Message):
    """Handle the /song command."""
    if len(message.command) < 2:
        return await message.reply_text("Please provide a song name or a link.")

    query = " ".join(message.command[1:])
    await message.reply_text("Downloading your song, please wait...")

    song_path = download_song(query)

    if not song_path:
        return await message.reply_text("Could not download the song.")

    await message.reply_audio(audio=song_path)
    await client.send_message(
        LOG_GROUP_ID,
        f"**Download Log**\n\n"
        f"**User:** {message.from_user.mention}\n"
        f"**Username:** @{message.from_user.username}\n"
        f"**User ID:** `{message.from_user.id}`\n"
        f"**Song:** {os.path.basename(song_path)}",
    )
    os.remove(song_path)
