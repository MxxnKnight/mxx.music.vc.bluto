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

import asyncio
from pyrogram import Client, idle
from pytgcalls import PyTgCalls

from Bluto.config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    SESSION_NAME,
    LOG_GROUP_ID
)
from Bluto.logging import LOGGER


# Pyrogram Client
app = Client(
    name=SESSION_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# Pytgcalls Client
pytgcalls = PyTgCalls(app)


async def main():
    """
    Asynchronous main function to start the bot, initialize clients,
    and keep the bot running.
    """
    LOGGER(__name__).info("Starting Bluto Bot...")
    await app.start()
    LOGGER(__name__).info("Pyrogram Client Started.")

    LOGGER(__name__).info("Starting Pytgcalls Client...")
    await pytgcalls.start()
    LOGGER(__name__).info("Pytgcalls Client Started.")

    await idle()
    LOGGER(__name__).info("Stopping Bluto Bot...")
    await app.stop()


if __name__ == "__main__":
    asyncio.run(main())
