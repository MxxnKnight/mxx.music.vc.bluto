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

from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os

def generate_thumbnail(title: str, thumbnail_url: str, duration: int, requested_by: str):
    """Generate a 'Now Playing' thumbnail."""
    try:
        # Create thumbnails directory if it doesn't exist
        if not os.path.isdir("thumbnails"):
            os.makedirs("thumbnails")

        # Download and open the thumbnail
        response = requests.get(thumbnail_url)
        img = Image.open(BytesIO(response.content)).convert("RGBA")

        # Create a drawing context
        draw = ImageDraw.Draw(img)

        # Font (assuming a font file is available)
        try:
            font = ImageFont.truetype("assets/font.ttf", 24)
            title_font = ImageFont.truetype("assets/font.ttf", 30)
        except IOError:
            font = ImageFont.load_default()
            title_font = ImageFont.load_default()

        # Add a semi-transparent overlay
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 128))
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)

        # Add title
        draw.text((20, 20), title, font=title_font, fill="white")

        # Add duration
        duration_str = f"{duration // 60}:{duration % 60:02d}"
        draw.text((20, img.height - 60), f"Duration: {duration_str}", font=font, fill="white")

        # Add requested by
        draw.text((20, img.height - 90), f"Requested by: {requested_by}", font=font, fill="white")

        # Save the image
        path = f"thumbnails/thumb_{title}.png"
        img.save(path)
        return path
    except Exception as e:
        print(f"Failed to generate thumbnail: {e}")
        return None
