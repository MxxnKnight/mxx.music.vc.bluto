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
from typing import Union
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import StreamType
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)

from Bluto.bot import pytgcalls, app
from Bluto.config import (
    LOG_GROUP_ID,
    STREAM_ENABLED,
    VIDEO_STREAM_LIMIT,
)
from Bluto.logging import LOGGER

class BlutoPlayer:
    def __init__(self):
        self._groups = {}

    async def _update_stream(self, chat_id: int, stream: Update):
        """Callback function to handle stream updates."""
        if isinstance(stream, Update.StreamEnded):
            LOGGER(__name__).info(f"Stream ended in chat {chat_id}")
            if self._groups[chat_id]["queue"]:
                next_song = self._groups[chat_id]["queue"].pop(0)
                await self.play(chat_id, next_song["url"], is_video=next_song["is_video"])
                try:
                    await app.send_message(chat_id, f"Now playing: {next_song['title']}")
                except Exception as e:
                    LOGGER(__name__).error(f"Failed to send message: {e}")
            else:
                self._groups[chat_id]["status"] = "inactive"
                await self.leave_vc(chat_id)

    async def join_vc(self, chat_id: int, user_id: int):
        """Join a voice chat."""
        if chat_id in self._groups:
            return "already_in_vc"

        self._groups[chat_id] = {
            "user_id": user_id,
            "status": "inactive",
            "queue": [],
        }
        await pytgcalls.join_group_call(
            chat_id,
            AudioPiped(""), # A dummy stream to join
            stream_type=StreamType().pulse_stream,
        )
        LOGGER(__name__).info(f"Joined VC in chat {chat_id}")

    async def leave_vc(self, chat_id: int):
        """Leave a voice chat."""
        if chat_id not in self._groups:
            return "not_in_vc"

        await pytgcalls.leave_group_call(chat_id)
        del self._groups[chat_id]
        LOGGER(__name__).info(f"Left VC in chat {chat_id}")

    async def play(self, chat_id: int, song_path: str, is_video: bool = False):
        """Play a song."""
        if chat_id not in self._groups:
            return "not_in_vc"

        stream_quality = (
            HighQualityVideo() if is_video else HighQualityAudio()
        )
        stream = (
            AudioVideoPiped(song_path, video_parameters=stream_quality)
            if is_video
            else AudioPiped(song_path, audio_parameters=stream_quality)
        )

        await pytgcalls.change_stream(chat_id, stream)
        self._groups[chat_id]["status"] = "playing"
        LOGGER(__name__).info(f"Playing {'video' if is_video else 'audio'} in chat {chat_id}")

    async def pause(self, chat_id: int):
        """Pause playback."""
        if chat_id not in self._groups or self._groups[chat_id]["status"] != "playing":
            return "nothing_playing"

        await pytgcalls.pause_stream(chat_id)
        self._groups[chat_id]["status"] = "paused"
        LOGGER(__name__).info(f"Paused playback in chat {chat_id}")

    async def resume(self, chat_id: int):
        """Resume playback."""
        if chat_id not in self._groups or self._groups[chat_id]["status"] != "paused":
            return "nothing_paused"

        await pytgcalls.resume_stream(chat_id)
        self._groups[chat_id]["status"] = "playing"
        LOGGER(__name__).info(f"Resumed playback in chat {chat_id}")

    async def stop(self, chat_id: int):
        """Stop playback."""
        if chat_id not in self._groups:
            return "not_in_vc"

        await pytgcalls.change_stream(chat_id, AudioPiped("")) # Stop by playing silence
        self._groups[chat_id]["status"] = "inactive"
        LOGGER(__name__).info(f"Stopped playback in chat {chat_id}")

    def get_queue(self, chat_id: int):
        """Get the queue for a chat."""
        return self._groups.get(chat_id, {}).get("queue", [])

    def add_to_queue(self, chat_id: int, song_details: dict):
        """Add a song to the queue."""
        if chat_id in self._groups:
            self._groups[chat_id]["queue"].append(song_details)
            return "added_to_queue"
        return "not_in_vc"

    def clear_queue(self, chat_id: int):
        """Clear the queue for a chat."""
        if chat_id in self._groups:
            self._groups[chat_id]["queue"].clear()
            return "queue_cleared"
        return "not_in_vc"

    def shuffle_queue(self, chat_id: int):
        """Shuffle the queue for a chat."""
        if chat_id in self._groups and self._groups[chat_id]["queue"]:
            import random
            random.shuffle(self._groups[chat_id]["queue"])
            return "queue_shuffled"
        return "queue_empty"

bluto_player = BlutoPlayer()
pytgcalls.on_stream_end()(bluto_player._update_stream)
