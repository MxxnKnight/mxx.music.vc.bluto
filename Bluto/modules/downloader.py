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
import uuid
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from Bluto.bot import app
from Bluto.config import LOG_GROUP_ID, BOT_USERNAME, FORCE_SUB_CHANNEL, LOG_TOPIC_ID
from Bluto.helpers.decorators import is_banned, force_subscribe
from Bluto.helpers.database import (
    is_song_download_enabled,
    create_song_request,
    get_song_request,
    delete_song_request,
)
from Bluto.helpers.youtube import get_song_stream, get_video_info
import aiohttp
from io import BytesIO


@app.on_message(filters.command("song"))
@is_banned
@force_subscribe
async def song_command(client: Client, message: Message):
    """Handle the /song command."""
    if len(message.command) < 2:
        return await message.reply_text("Please provide a song name or a link.")

    query = " ".join(message.command[1:])

    if message.chat.type == "group" and await is_song_download_enabled(message.chat.id):
        status_message = await message.reply_text("Processing your request...")

        video_info = get_video_info(query)
        if not video_info:
            return await status_message.edit_text("Could not find the song.")

        request_id = str(uuid.uuid4())
        await create_song_request(
            request_id,
            message.from_user.id,
            query,
            message.chat.id,
            status_message.id,
        )

        await status_message.edit_text(
            f"**Song:** {video_info['title']}\n\n"
            "Click the button below to get the song.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Get Song",
                            callback_data=f"get_song_{request_id}",
                        )
                    ]
                ]
            ),
        )
        return

    else:
        status_message = await message.reply_text(
            "Downloading your song, please wait..."
        )
        song_stream = get_song_stream(query)

        if not song_stream:
            return await status_message.edit_text("Could not download the song.")

        async with aiohttp.ClientSession() as session:
            async with session.get(song_stream["url"]) as resp:
                if resp.status == 200:
                    audio_buffer = BytesIO(await resp.read())
                    audio_buffer.name = f"{song_stream['title']}.mp3"
                    await message.reply_audio(audio=audio_buffer)
                    await client.send_message(
                        LOG_GROUP_ID,
                        f"**Download Log**\n\n"
                        f"**User:** {message.from_user.mention}\n"
                        f"**Username:** @{message.from_user.username}\n"
                        f"**User ID:** `{message.from_user.id}`\n"
                        f"**Song:** {song_stream['title']}",
                        message_thread_id=LOG_TOPIC_ID,
                    )
                    await status_message.delete()
                else:
                    await status_message.edit_text("Could not download the song.")


async def send_song(client: Client, user_id: int, song_request: dict):
    """Download and send the song."""
    status_message = await client.send_message(
        user_id, "Downloading your song, please wait..."
    )
    song_stream = get_song_stream(song_request["query"])

    if not song_stream:
        return await status_message.edit_text("Could not download the song.")

    async with aiohttp.ClientSession() as session:
        async with session.get(song_stream["url"]) as resp:
            if resp.status == 200:
                audio_buffer = BytesIO(await resp.read())
                audio_buffer.name = f"{song_stream['title']}.mp3"
                await client.send_audio(user_id, audio=audio_buffer)
                await status_message.delete()
                await delete_song_request(song_request["request_id"])
            else:
                await status_message.edit_text("Could not download the song.")


@app.on_callback_query(filters.regex("^get_song_"))
async def get_song_callback(client: Client, callback_query: CallbackQuery):
    """Handle the get_song callback query."""
    request_id = callback_query.data.split("_")[2]
    song_request = await get_song_request(request_id)

    if not song_request:
        return await callback_query.answer(
            "This request is invalid or has expired.", show_alert=True
        )

    if callback_query.from_user.id != song_request["user_id"]:
        return await callback_query.answer(
            "This button is not for you.", show_alert=True
        )

    await callback_query.answer("The song will be sent to your PM.", show_alert=True)
    await client.delete_messages(
        chat_id=song_request["chat_id"], message_ids=song_request["message_id"]
    )

    try:
        member = await client.get_chat_member(
            FORCE_SUB_CHANNEL, callback_query.from_user.id
        )
        if member.status in ["kicked", "left"]:
            return await client.send_message(
                callback_query.from_user.id,
                "You must join my updates channel to use me.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Join Channel", url=f"https://t.me/{FORCE_SUB_CHANNEL}"
                            ),
                            InlineKeyboardButton(
                                "Recheck", callback_data=f"recheck_song_{request_id}"
                            ),
                        ]
                    ]
                ),
            )
    except Exception as e:
        return await client.send_message(
            callback_query.from_user.id,
            f"Something went wrong while checking your subscription: {e}",
        )

    await send_song(client, callback_query.from_user.id, song_request)


@app.on_callback_query(filters.regex("^recheck_song_"))
async def recheck_song_subscription(client: Client, callback_query: CallbackQuery):
    """Handle the recheck_song callback query."""
    request_id = callback_query.data.split("_")[2]
    song_request = await get_song_request(request_id)

    if not song_request:
        return await callback_query.answer(
            "This request is invalid or has expired.", show_alert=True
        )

    if callback_query.from_user.id != song_request["user_id"]:
        return await callback_query.answer(
            "This button is not for you.", show_alert=True
        )

    try:
        member = await client.get_chat_member(
            FORCE_SUB_CHANNEL, callback_query.from_user.id
        )
        if member.status in ["kicked", "left"]:
            return await callback_query.answer(
                "You still haven't joined the channel.", show_alert=True
            )
    except Exception as e:
        return await callback_query.answer(
            f"Something went wrong while checking your subscription: {e}",
            show_alert=True,
        )

    await callback_query.message.delete()
    await send_song(client, callback_query.from_user.id, song_request)
