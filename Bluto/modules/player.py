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
from Bluto.config import BOT_USERNAME
from Bluto.pytgcalls.player import bluto_player
from Bluto.helpers.youtube import search, get_video_info
from Bluto.helpers.thumbnail import generate_thumbnail
from Bluto.helpers.decorators import admin_only


@app.on_message(filters.command(["play", f"play@{BOT_USERNAME}"]))
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

    if bluto_player._groups[message.chat.id]["status"] != "playing":
        await bluto_player.play(message.chat.id, video_info["url"], is_video=video_info["is_video"])

        # Generate and send thumbnail
        thumbnail_path = generate_thumbnail(video_info['title'], video_info['thumbnail'], video_info['duration'], 0)
        if thumbnail_path:
            await message.reply_photo(
                photo=thumbnail_path,
                caption=f"Now playing: {video_info['title']}"
            )
            import os
            os.remove(thumbnail_path)
        else:
            await message.reply_text(f"Now playing: {video_info['title']}")
    else:
        await message.reply_text(f"Added to queue: {video_info['title']}")


@app.on_message(filters.command(["pause", f"pause@{BOT_USERNAME}"]))
@admin_only
async def pause_command(client: Client, message: Message):
    """Handle the /pause command."""
    result = await bluto_player.pause(message.chat.id)
    if result == "nothing_playing":
        await message.reply_text("Nothing is playing.")
    else:
        await message.reply_text("Paused playback.")


@app.on_message(filters.command(["resume", f"resume@{BOT_USERNAME}"]))
@admin_only
async def resume_command(client: Client, message: Message):
    """Handle the /resume command."""
    result = await bluto_player.resume(message.chat.id)
    if result == "nothing_paused":
        await message.reply_text("Nothing is paused.")
    else:
        await message.reply_text("Resumed playback.")


@app.on_message(filters.command(["skip", f"skip@{BOT_USERNAME}"]))
@admin_only
async def skip_command(client: Client, message: Message):
    """Handle the /skip command."""
    if not bluto_player.get_queue(message.chat.id):
        return await message.reply_text("The queue is empty.")

    await bluto_player.stop(message.chat.id)
    await message.reply_text("Skipped to the next song.")


@app.on_message(filters.command(["end", "stop", f"end@{BOT_USERNAME}", f"stop@{BOT_USERNAME}"]))
@admin_only
async def end_command(client: Client, message: Message):
    """Handle the /end and /stop commands."""
    await bluto_player.stop(message.chat.id)
    await bluto_player.leave_vc(message.chat.id)
    await message.reply_text("Stopped playback and left the voice chat.")


@app.on_message(filters.command(["queue", f"queue@{BOT_USERNAME}"]))
async def queue_command(client: Client, message: Message):
    """Handle the /queue command."""
    queue = bluto_player.get_queue(message.chat.id)
    if not queue:
        return await message.reply_text("The queue is empty.")

    queue_list = "\n".join([f"{i+1}. {song['title']}" for i, song in enumerate(queue)])
    await message.reply_text(f"**Queue:**\n{queue_list}")


@app.on_message(filters.command(["clearqueue", f"clearqueue@{BOT_USERNAME}"]))
@admin_only
async def clear_queue_command(client: Client, message: Message):
    """Handle the /clearqueue command."""
    result = bluto_player.clear_queue(message.chat.id)
    if result == "queue_cleared":
        await message.reply_text("Queue cleared.")
    else:
        await message.reply_text("Nothing to clear.")


@app.on_message(filters.command(["shuffle", f"shuffle@{BOT_USERNAME}"]))
@admin_only
async def shuffle_command(client: Client, message: Message):
    """Handle the /shuffle command."""
    result = bluto_player.shuffle_queue(message.chat.id)
    if result == "queue_shuffled":
        await message.reply_text("Queue shuffled.")
    else:
        await message.reply_text("The queue is empty.")
