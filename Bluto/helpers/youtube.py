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

import yt_dlp
from youtube_search import YoutubeSearch

def search(query: str, limit: int = 10):
    """Search for videos on YouTube."""
    try:
        results = YoutubeSearch(query, max_results=limit).to_dict()
        return results
    except Exception as e:
        print(f"YouTube search failed: {e}")
        return []

def get_video_info(url: str):
    """Get video information from a URL."""
    if "open.spotify.com" in url:
        ydl_opts = {
            'noplaylist': True,
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                query = f"{info['artist']} - {info['track']}"
                return get_video_info(query)
            except Exception as e:
                print(f"Failed to get Spotify info: {e}")
                return None

    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)

            # Find the best audio stream URL
            audio_url = None
            for f in info.get('formats', []):
                if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                    audio_url = f.get('url')
                    break

            # If no audio-only stream, take the best available
            if not audio_url:
                audio_url = info.get('url')

            return {
                "title": info.get("title", "Unknown Title"),
                "duration": info.get("duration", 0),
                "thumbnail": info.get("thumbnail", None),
                "url": audio_url,
                "is_video": info.get("is_live", False) or info.get("duration", 0) > 0,
            }
        except Exception as e:
            print(f"Failed to get video info: {e}")
            return None


def download_song(url: str):
    """Download a song from a URL."""
    from Bluto.config import AUDIO_FORMAT
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': AUDIO_FORMAT,
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
        except Exception as e:
            print(f"Failed to download song: {e}")
            return None
