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
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from Bluto.bot import app
from Bluto.config import LOG_GROUP_ID, LOG_TOPIC_ID
from Bluto.helpers.decorators import admin_only
from Bluto.helpers.database import (
    ban_user as ban_user_db,
    unban_user as unban_user_db,
    is_song_download_enabled,
    enable_song_download,
    disable_song_download,
)


async def get_user_from_message(message: Message):
    """Get user from message."""
    if message.reply_to_message:
        return message.reply_to_message.from_user
    if len(message.command) > 1:
        try:
            if message.command[1].isdigit():
                return await app.get_users(int(message.command[1]))
            else:
                return await app.get_users(message.command[1])
        except Exception:
            return None
    return None


@app.on_message(filters.command("warn"))
@admin_only
async def warn_user(client: Client, message: Message):
    """Warn a user."""
    user_to_warn = await get_user_from_message(message)
    if not user_to_warn:
        return await message.reply_text("Please reply to a user or provide a user ID.")

    warning_message = (
        f"**Warning**\n\n"
        f"You have received a warning from the admin of this bot. "
        f"Please refrain from misusing the bot, or you may be banned."
    )
    try:
        await client.send_message(user_to_warn.id, warning_message)
        await message.reply_text(f"Warning sent to {user_to_warn.mention}.")
        await client.send_message(
            LOG_GROUP_ID,
            f"**Warn Log**\n\n"
            f"**Admin:** {message.from_user.mention}\n"
            f"**User:** {user_to_warn.mention}\n"
            f"**User ID:** `{user_to_warn.id}`",
            message_thread_id=LOG_TOPIC_ID,
        )
    except Exception as e:
        await message.reply_text(f"Failed to send warning: {e}")


@app.on_message(filters.command("ban"))
@admin_only
async def ban_user(client: Client, message: Message):
    """Ban a user."""
    user_to_ban = await get_user_from_message(message)
    if not user_to_ban:
        return await message.reply_text("Please reply to a user or provide a user ID.")

    await ban_user_db(user_to_ban.id)
    await message.reply_text(f"{user_to_ban.mention} has been banned.")
    await client.send_message(
        LOG_GROUP_ID,
        f"**Ban Log**\n\n"
        f"**Admin:** {message.from_user.mention}\n"
        f"**User:** {user_to_ban.mention}\n"
        f"**User ID:** `{user_to_ban.id}`",
        message_thread_id=LOG_TOPIC_ID,
    )


@app.on_message(filters.command("unban"))
@admin_only
async def unban_user(client: Client, message: Message):
    """Unban a user."""
    user_to_unban = await get_user_from_message(message)
    if not user_to_unban:
        return await message.reply_text("Please reply to a user or provide a user ID.")

    await unban_user_db(user_to_unban.id)
    await message.reply_text(f"{user_to_unban.mention} has been unbanned.")
    await client.send_message(
        LOG_GROUP_ID,
        f"**Unban Log**\n\n"
        f"**Admin:** {message.from_user.mention}\n"
        f"**User:** {user_to_unban.mention}\n"
        f"**User ID:** `{user_to_unban.id}`",
        message_thread_id=LOG_TOPIC_ID,
    )


@app.on_message(filters.command("songstatus") & filters.private)
@admin_only
async def song_status(client: Client, message: Message):
    """Get the song download status for a chat."""
    if len(message.command) < 2:
        return await message.reply_text("Please provide a chat ID.")

    chat_id = int(message.command[1])
    is_enabled = await is_song_download_enabled(chat_id)
    status = "Enabled" if is_enabled else "Disabled"

    await message.reply_text(
        f"**Song Download Status for {chat_id}**\n\n" f"**Status:** {status}",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Enable", callback_data=f"enablesong_{chat_id}"
                    ),
                    InlineKeyboardButton(
                        text="Disable", callback_data=f"disablesong_{chat_id}"
                    ),
                ]
            ]
        ),
    )


@app.on_callback_query(filters.regex("^enablesong_"))
@admin_only
async def enable_song_callback(client: Client, callback_query: CallbackQuery):
    """Handle the enable song callback query."""
    chat_id = int(callback_query.data.split("_")[1])
    await enable_song_download(chat_id)
    await callback_query.message.edit_text(
        f"**Song Download Status for {chat_id}**\n\n" f"**Status:** Enabled",
        reply_markup=callback_query.message.reply_markup,
    )
    await callback_query.answer("Song download enabled.")


@app.on_callback_query(filters.regex("^disablesong_"))
@admin_only
async def disable_song_callback(client: Client, callback_query: CallbackQuery):
    """Handle the disable song callback query."""
    chat_id = int(callback_query.data.split("_")[1])
    await disable_song_download(chat_id)
    await callback_query.message.edit_text(
        f"**Song Download Status for {chat_id}**\n\n" f"**Status:** Disabled",
        reply_markup=callback_query.message.reply_markup,
    )
    await callback_query.answer("Song download disabled.")
