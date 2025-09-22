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

def owner_only(func):
    @wraps(func)
    async def wrapper(client: Client, update):
        if isinstance(update, Message):
            user = update.from_user
        elif isinstance(update, CallbackQuery):
            user = update.from_user
        else:
            return

        if user.id != OWNER_ID:
            if isinstance(update, Message):
                await update.reply_text("This command is for the owner only.")
            elif isinstance(update, CallbackQuery):
                await update.answer("This command is for the owner only.", show_alert=True)
            return
        return await func(client, update)
    return wrapper

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Bluto.config import FORCE_SUB_CHANNEL
from Bluto.helpers.database import is_user_banned

def admin_only(func):
    @wraps(func)
    async def wrapper(client: Client, update):
        if isinstance(update, Message):
            user = update.from_user
            chat_id = update.chat.id
        elif isinstance(update, CallbackQuery):
            user = update.from_user
            chat_id = update.message.chat.id
        else:
            return

        if user.id in SUDO_USERS:
            return await func(client, update)

        chat_member = await client.get_chat_member(chat_id=chat_id, user_id=user.id)
        if chat_member.status not in ["administrator", "creator"]:
            if isinstance(update, Message):
                await update.reply_text("You are not an admin.")
            elif isinstance(update, CallbackQuery):
                await update.answer("You are not an admin.", show_alert=True)
            return
        return await func(client, update)
    return wrapper


def is_banned(func):
    @wraps(func)
    async def wrapper(client: Client, update):
        if isinstance(update, Message):
            user = update.from_user
        elif isinstance(update, CallbackQuery):
            user = update.from_user
        else:
            return

        if await is_user_banned(user.id):
            if isinstance(update, Message):
                await update.reply_text("You are banned from using this bot.")
            elif isinstance(update, CallbackQuery):
                await update.answer("You are banned from using this bot.", show_alert=True)
            return
        return await func(client, update)
    return wrapper


def force_subscribe(func):
    @wraps(func)
    async def wrapper(client: Client, update):
        if not FORCE_SUB_CHANNEL:
            return await func(client, update)

        if isinstance(update, Message):
            user = update.from_user
        elif isinstance(update, CallbackQuery):
            user = update.from_user
        else:
            return

        try:
            member = await client.get_chat_member(FORCE_SUB_CHANNEL, user.id)
            if member.status in ["kicked", "left"]:
                if isinstance(update, Message):
                    await update.reply_text(
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
                elif isinstance(update, CallbackQuery):
                    await update.answer(
                        "You must join my updates channel to use me.", show_alert=True
                    )
                return
        except Exception:
            if isinstance(update, Message):
                await update.reply_text(
                    "Something went wrong. Make sure I am an admin in the force subscribe channel."
                )
            elif isinstance(update, CallbackQuery):
                await update.answer(
                    "Something went wrong. Make sure I am an admin in the force subscribe channel.",
                    show_alert=True,
                )
            return
        return await func(client, update)
    return wrapper
