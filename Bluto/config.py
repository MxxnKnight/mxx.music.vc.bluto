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
from os import getenv
from dotenv import load_dotenv


load_dotenv()

# Get it from my.telegram.org
API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH", "")

# Get it from @Botfather in Telegram.
BOT_TOKEN = getenv("BOT_TOKEN", "")

# Database to save your chats and stats...
DATABASE_URL = getenv("DATABASE_URL", "")

# SUDO USERS
SUDO_USERS = list(
    map(int, getenv("SUDO_USERS", "").split())
)  # Input type must be interger.

# You'll need a Private Group for this.
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", ""))

# Message to display when someone starts your bot
PRIVATE_START_MESSAGE = getenv(
    "PRIVATE_START_MESSAGE",
    "Hello! I am Bluto, a bot designed to play music in VC.",
)

# Your Bot's Username.
BOT_USERNAME = getenv("BOT_USERNAME", "")

# Get this from @FallenIdsBot
OWNER_ID = int(getenv("OWNER_ID", ""))

# Git Repo details
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/Mxx-x/Bluto")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "master")

# Support Links
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/BlutoUpdates")
SUPPORT_GROUP = getenv("SUPPORT_GROUP", "https://t.me/BlutoSupport")


# Enable or disable platform streamings
STREAM_ENABLED = getenv("STREAM_ENABLED", "True").lower() == "true"

# Maximum video length which can be streamed
VIDEO_STREAM_LIMIT = int(getenv("VIDEO_STREAM_LIMIT", "60")) # In minutes

# Pyrogram Session
SESSION_NAME = getenv("SESSION_NAME", "Bluto")

# Force Subscribe Channel
FORCE_SUB_CHANNEL = getenv("FORCE_SUB_CHANNEL", "")
