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

from functools import wraps
from pyrogram.types import Message
from pyrogram import Client

from Bluto.config import OWNER_ID, SUDO_USERS
from Bluto.helpers.database import is_user_banned


def owner_only(func):
    @wraps(func)
    async def wrapper(client: Client, message: Message):
        if message.from_user.id != OWNER_ID:
            return await message.reply_text("This command is for the owner only.")
        return await func(client, message)
    return wrapper


def admin_only(func):
    @wraps(func)
    async def wrapper(client: Client, message: Message):
        if message.from_user.id in SUDO_USERS or message.from_user.id == OWNER_ID:
            return await func(client, message)

        chat_member = await client.get_chat_member(
            chat_id=message.chat.id, user_id=message.from_user.id
        )
        if chat_member.status not in ["administrator", "creator"]:
            return await message.reply_text("You are not an admin.")
        return await func(client, message)
    return wrapper


def is_banned(func):
    @wraps(func)
    async def wrapper(client: Client, message: Message):
        if await is_user_banned(message.from_user.id):
            return await message.reply_text("You are banned from using this bot.")
        return await func(client, message)
    return wrapper


def force_subscribe(func):
    @wraps(func)
    async def wrapper(client: Client, message: Message):
        from Bluto.config import FORCE_SUB_CHANNEL
        if not FORCE_SUB_CHANNEL:
            return await func(client, message)
        try:
            member = await client.get_chat_member(FORCE_SUB_CHANNEL, message.from_user.id)
            if member.status in ["kicked", "left"]:
                await message.reply_text(
                    "You must join my updates channel to use me.",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Join Channel", url=f"https://t.me/{FORCE_SUB_CHANNEL}"
                                )
                            ]
                        ]
                    ),
                )
                return
        except Exception:
            await message.reply_text(
                "Something went wrong. Make sure I am an admin in the force subscribe channel."
            )
            return
        return await func(client, message)
    return wrapper
