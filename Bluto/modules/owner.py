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

from pyrogram import Client, filters
from pyrogram.types import Message

from Bluto.bot import app
from Bluto.helpers.decorators import owner_only
from Bluto.helpers.database import (
    enable_song_download,
    disable_song_download,
)


@app.on_message(filters.command("enablesong") & filters.group)
@owner_only
async def enable_song(client: Client, message: Message):
    """Enable song download in a chat."""
    await enable_song_download(message.chat.id)
    await message.reply_text("Song download has been enabled for this chat.")


@app.on_message(filters.command("disablesong") & filters.group)
@owner_only
async def disable_song(client: Client, message: Message):
    """Disable song download in a chat."""
    await disable_song_download(message.chat.id)
    await message.reply_text("Song download has been disabled for this chat.")
