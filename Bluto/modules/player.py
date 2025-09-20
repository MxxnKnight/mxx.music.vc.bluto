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
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from Bluto.bot import app
from Bluto.config import BOT_USERNAME, LOG_GROUP_ID
from Bluto.pytgcalls.player import bluto_player
from Bluto.helpers.youtube import search, get_video_info
from Bluto.helpers.thumbnail import generate_thumbnail
from Bluto.helpers.decorators import admin_only, is_banned

# Constants for callback data
PAUSE_CALLBACK = "pause"
RESUME_CALLBACK = "resume"
SKIP_CALLBACK = "skip"
STOP_CALLBACK = "stop"


def get_playback_keyboard(is_paused: bool) -> InlineKeyboardMarkup:
    """Get the playback control keyboard."""
    if is_paused:
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Resume", callback_data=RESUME_CALLBACK),
                    InlineKeyboardButton(text="Skip", callback_data=SKIP_CALLBACK),
                    InlineKeyboardButton(text="Stop", callback_data=STOP_CALLBACK),
                ]
            ]
        )
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Pause", callback_data=PAUSE_CALLBACK),
                InlineKeyboardButton(text="Skip", callback_data=SKIP_CALLBACK),
                InlineKeyboardButton(text="Stop", callback_data=STOP_CALLBACK),
            ]
        ]
    )


@app.on_message(filters.command(["play", f"play@{BOT_USERNAME}"]))
@is_banned
async def play_command(client: Client, message: Message):
    """Handle the /play command."""
    if len(message.command) < 2:
        return await message.reply_text("Please provide a song name or a YouTube link.")

    query = " ".join(message.command[1:])

    # Join the voice chat
    await bluto_player.join_vc(message.chat.id, message.from_user.id)

    # Search for the song
    video_info = None
    if "http" in query:
        video_info = get_video_info(query)
    else:
        search_results = search(query, limit=1)
        if search_results:
            video_info = get_video_info(search_results[0]["link"])

    if not video_info or not video_info["url"]:
        return await message.reply_text("Could not find the song.")

    # Add to queue and play
    await bluto_player.add_to_queue(message.chat.id, video_info)

    if bluto_player._groups.get(message.chat.id, {}).get("status") != "playing":
        await bluto_player.play(
            message.chat.id, video_info["url"], is_video=video_info["is_video"]
        )

        # Log the action
        await client.send_message(
            LOG_GROUP_ID,
            f"**Play Log**\n\n"
            f"**User:** {message.from_user.mention}\n"
            f"**Username:** @{message.from_user.username}\n"
            f"**User ID:** `{message.from_user.id}`\n"
            f"**Song:** {video_info['title']}",
        )

        # Generate and send thumbnail
        thumbnail_path = generate_thumbnail(
            video_info["title"], video_info["thumbnail"], video_info["duration"], 0
        )
        if thumbnail_path:
            await message.reply_photo(
                photo=thumbnail_path,
                caption=f"Now playing: {video_info['title']}",
                reply_markup=get_playback_keyboard(False),
            )
            import os

            os.remove(thumbnail_path)
        else:
            await message.reply_text(
                f"Now playing: {video_info['title']}",
                reply_markup=get_playback_keyboard(False),
            )
    else:
        await message.reply_text(f"Added to queue: {video_info['title']}")


@app.on_message(filters.command(["playnow", f"playnow@{BOT_USERNAME}"]))
@admin_only
async def playnow_command(client: Client, message: Message):
    """Handle the /playnow command."""
    if len(message.command) < 2:
        return await message.reply_text("Please provide a song name or a YouTube link.")

    query = " ".join(message.command[1:])

    # Join the voice chat
    await bluto_player.join_vc(message.chat.id, message.from_user.id)

    # Search for the song
    video_info = None
    if "http" in query:
        video_info = get_video_info(query)
    else:
        search_results = search(query, limit=1)
        if search_results:
            video_info = get_video_info(search_results[0]["link"])

    if not video_info or not video_info["url"]:
        return await message.reply_text("Could not find the song.")

    # Add to queue and play
    await bluto_player.add_to_queue(message.chat.id, video_info, at_front=True)
    await bluto_player.play(
        message.chat.id, video_info["url"], is_video=video_info["is_video"]
    )

    # Log the action
    await client.send_message(
        LOG_GROUP_ID,
        f"**Play Log (Admin)**\n\n"
        f"**User:** {message.from_user.mention}\n"
        f"**Username:** @{message.from_user.username}\n"
        f"**User ID:** `{message.from_user.id}`\n"
        f"**Song:** {video_info['title']}",
    )

    # Generate and send thumbnail
    thumbnail_path = generate_thumbnail(
        video_info["title"], video_info["thumbnail"], video_info["duration"], 0
    )
    if thumbnail_path:
        await message.reply_photo(
            photo=thumbnail_path,
            caption=f"Now playing: {video_info['title']}",
            reply_markup=get_playback_keyboard(False),
        )
        import os

        os.remove(thumbnail_path)
    else:
        await message.reply_text(
            f"Now playing: {video_info['title']}",
            reply_markup=get_playback_keyboard(False),
        )


@app.on_message(filters.command(["pause", f"pause@{BOT_USERNAME}"]))
@admin_only
@is_banned
async def pause_command(client: Client, message: Message):
    """Handle the /pause command."""
    result = await bluto_player.pause(message.chat.id)
    if result == "nothing_playing":
        await message.reply_text("Nothing is playing.")
    else:
        await message.reply_text("Paused playback.")
        # This will only work if the message is a reply to the bot's "now playing" message
        if message.reply_to_message and message.reply_to_message.from_user.is_self:
            await message.reply_to_message.edit_reply_markup(get_playback_keyboard(True))


@app.on_message(filters.command(["resume", f"resume@{BOT_USERNAME}"]))
@admin_only
@is_banned
async def resume_command(client: Client, message: Message):
    """Handle the /resume command."""
    result = await bluto_player.resume(message.chat.id)
    if result == "nothing_paused":
        await message.reply_text("Nothing is paused.")
    else:
        await message.reply_text("Resumed playback.")
        # This will only work if the message is a reply to the bot's "now playing" message
        if message.reply_to_message and message.reply_to_message.from_user.is_self:
            await message.reply_to_message.edit_reply_markup(get_playback_keyboard(False))


@app.on_message(filters.command(["skip", f"skip@{BOT_USERNAME}"]))
@admin_only
@is_banned
async def skip_command(client: Client, message: Message):
    """Handle the /skip command."""
    if not bluto_player.get_queue(message.chat.id):
        return await message.reply_text("The queue is empty.")

    await bluto_player.stop(message.chat.id)
    await message.reply_text("Skipped to the next song.")


@app.on_message(filters.command(["end", "stop", f"end@{BOT_USERNAME}", f"stop@{BOT_USERNAME}"]))
@admin_only
@is_banned
async def end_command(client: Client, message: Message):
    """Handle the /end and /stop commands."""
    await bluto_player.stop(message.chat.id)
    await bluto_player.leave_vc(message.chat.id)
    await message.reply_text("Stopped playback and left the voice chat.")


@app.on_message(filters.command(["queue", f"queue@{BOT_USERNAME}"]))
@is_banned
async def queue_command(client: Client, message: Message):
    """Handle the /queue command."""
    queue = bluto_player.get_queue(message.chat.id)
    if not queue:
        return await message.reply_text("The queue is empty.")

    queue_list = "\n".join([f"{i+1}. {song['title']}" for i, song in enumerate(queue)])
    await message.reply_text(f"**Queue:**\n{queue_list}")


@app.on_message(filters.command(["clearqueue", f"clearqueue@{BOT_USERNAME}"]))
@admin_only
@is_banned
async def clear_queue_command(client: Client, message: Message):
    """Handle the /clearqueue command."""
    result = bluto_player.clear_queue(message.chat.id)
    if result == "queue_cleared":
        await message.reply_text("Queue cleared.")
    else:
        await message.reply_text("Nothing to clear.")


@app.on_message(filters.command(["shuffle", f"shuffle@{BOT_USERNAME}"]))
@admin_only
@is_banned
async def shuffle_command(client: Client, message: Message):
    """Handle the /shuffle command."""
    result = bluto_player.shuffle_queue(message.chat.id)
    if result == "queue_shuffled":
        await message.reply_text("Queue shuffled.")
    else:
        await message.reply_text("The queue is empty.")


@app.on_callback_query(filters.regex(f"^{PAUSE_CALLBACK}$"))
@admin_only
async def pause_callback(client: Client, callback_query: CallbackQuery):
    """Handle the pause callback query."""
    result = await bluto_player.pause(callback_query.message.chat.id)
    if result == "nothing_playing":
        await callback_query.answer("Nothing is playing.")
    else:
        await callback_query.answer("Paused playback.")
        await callback_query.message.edit_reply_markup(get_playback_keyboard(True))


@app.on_callback_query(filters.regex(f"^{RESUME_CALLBACK}$"))
@admin_only
async def resume_callback(client: Client, callback_query: CallbackQuery):
    """Handle the resume callback query."""
    result = await bluto_player.resume(callback_query.message.chat.id)
    if result == "nothing_paused":
        await callback_query.answer("Nothing is paused.")
    else:
        await callback_query.answer("Resumed playback.")
        await callback_query.message.edit_reply_markup(get_playback_keyboard(False))


@app.on_callback_query(filters.regex(f"^{SKIP_CALLBACK}$"))
@admin_only
async def skip_callback(client: Client, callback_query: CallbackQuery):
    """Handle the skip callback query."""
    if not bluto_player.get_queue(callback_query.message.chat.id):
        return await callback_query.answer("The queue is empty.")

    await bluto_player.stop(callback_query.message.chat.id)
    await callback_query.answer("Skipped to the next song.")


@app.on_callback_query(filters.regex(f"^{STOP_CALLBACK}$"))
@admin_only
async def stop_callback(client: Client, callback_query: CallbackQuery):
    """Handle the stop callback query."""
    await bluto_player.stop(callback_query.message.chat.id)
    await bluto_player.leave_vc(callback_query.message.chat.id)
    await callback_query.answer("Stopped playback and left the voice chat.")
