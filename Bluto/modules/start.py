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
from Bluto.config import (
    BOT_USERNAME,
    PRIVATE_START_MESSAGE,
    SUPPORT_CHANNEL,
    SUPPORT_GROUP,
)

# Constants for callback data
ABOUT_CALLBACK = "about"
HELP_CALLBACK = "help"
BACK_CALLBACK = "back"


# Start menu keyboard
start_menu_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="About", callback_data=ABOUT_CALLBACK),
            InlineKeyboardButton(text="Help", callback_data=HELP_CALLBACK),
        ],
        [
            InlineKeyboardButton(text="Updates", url=SUPPORT_CHANNEL),
            InlineKeyboardButton(text="Support", url=SUPPORT_GROUP),
        ],
    ]
)

# About page keyboard
about_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="Help", callback_data=HELP_CALLBACK),
            InlineKeyboardButton(text="Back", callback_data=BACK_CALLBACK),
        ]
    ]
)

# Help page keyboard
help_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="About", callback_data=ABOUT_CALLBACK),
            InlineKeyboardButton(text="Back", callback_data=BACK_CALLBACK),
        ]
    ]
)


@app.on_message(filters.command(["start", f"start@{BOT_USERNAME}"]))
async def start_command(client: Client, message: Message):
    """Handle the /start command."""
    if message.chat.type == "private":
        await message.reply_text(
            PRIVATE_START_MESSAGE,
            reply_markup=start_menu_keyboard,
        )
    else:
        await message.reply_text(
            "Hello! I am running.",
        )


@app.on_callback_query(filters.regex(f"^{ABOUT_CALLBACK}$"))
async def about_page(client: Client, callback_query: CallbackQuery):
    """Display the about page."""
    await callback_query.message.edit_text(
        "**About Bluto Music Bot**\n\n"
        "Bluto is a powerful and easy-to-use music bot for Telegram. "
        "It allows you to play music in your group's voice chat from various sources, "
        "including YouTube, Spotify, and more.\n\n"
        "**Features:**\n"
        "- High-quality music playback\n"
        "- Queue system\n"
        "- Player controls\n"
        "- Admin controls\n"
        "- Support for multiple music sources\n\n"
        "Enjoy the music!",
        reply_markup=about_keyboard,
    )


@app.on_callback_query(filters.regex(f"^{HELP_CALLBACK}$"))
async def help_page(client: Client, callback_query: CallbackQuery):
    """Display the help page."""
    await callback_query.message.edit_text(
        "**Bluto Music Bot Help**\n\n"
        "Here are the available commands:\n\n"
        "**/play <song name or link>** - Plays a song.\n"
        "**/pause** - Pauses the music.\n"
        "**/resume** - Resumes the music.\n"
        "**/skip** - Skips the current song.\n"
        "**/end** or **/stop** - Stops the music and leaves the voice chat.\n"
        "**/queue** - Shows the list of songs in the queue.\n"
        "**/clearqueue** - Clears the queue.\n"
        "**/shuffle** - Shuffles the queue.\n\n"
        "**Admin Commands:**\n"
        "**/ban <user>** - Bans a user from using the bot.\n"
        "**/unban <user>** - Unbans a user.\n"
        "**/warn <user>** - Warns a user.\n",
        reply_markup=help_keyboard,
    )


@app.on_callback_query(filters.regex(f"^{BACK_CALLBACK}$"))
async def back_to_start_menu(client: Client, callback_query: CallbackQuery):
    """Return to the start menu."""
    await callback_query.message.edit_text(
        PRIVATE_START_MESSAGE,
        reply_markup=start_menu_keyboard,
    )
