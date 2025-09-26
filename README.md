# Bluto Music Bot

A Telegram VC Music Bot to play music in your group's voice chat.

## Features

- **Play from YouTube, Spotify, and YouTube Music:** Play any song from YouTube, Spotify, or YouTube Music by providing a link or by searching for the song name.
- **Song Download:** Download songs as audio files.
- **Advanced Group Download Flow:** In groups, the bot can be configured to send a private link to download the song, with a force-subscribe check.
- **Queue System:** Add multiple songs to a queue. The bot will automatically play the next song when the current one finishes.
- **Inline Player Controls:** Pause, resume, skip, and stop the music using inline buttons.
- **Admin Controls:** Admins can play music directly, stop playback, ban/unban users, and warn users.
- **"Now Playing" Thumbnail:** The bot sends a beautiful thumbnail with the song details when a song starts playing.
- **Force Subscribe:** Require users to join a channel before using the bot in private messages.
- **Logging:** Log all music playback and admin actions to a designated log channel, with support for topics.
- **Docker Support:** Easy to deploy using Docker.

## Deployment

### Prerequisites

1.  **API_ID and API_HASH:** Get these from [my.telegram.org](https://my.telegram.org).
2.  **BOT_TOKEN:** Get this from [@BotFather](https://t.me/BotFather) on Telegram.
3.  **DATABASE_URL:** Your PostgreSQL database URL.
4.  **OWNER_ID:** Your Telegram user ID. Get it from [@FallenIdsBot](https://t.me/FallenIdsBot).
5.  **LOG_GROUP_ID:** A private group ID for the bot to send logs.
6.  **LOG_TOPIC_ID:** The ID of the topic in the log group to send logs to (optional).
7.  **FORCE_SUB_CHANNEL:** The username of the channel that users must join to use the bot (optional).

### Configuration

Create a `.env` file with the following variables:

```
API_ID=
API_HASH=
BOT_TOKEN=
DATABASE_URL=
OWNER_ID=
LOG_GROUP_ID=
LOG_TOPIC_ID=
SUDO_USERS=
BOT_USERNAME= # Your bot's username without the @
SUPPORT_CHANNEL= # Your support channel link
SUPPORT_GROUP= # Your support group link
FORCE_SUB_CHANNEL= # The username of the force subscribe channel (without the @)
AUDIO_FORMAT= # The audio format for downloaded songs (e.g., mp3, m4a, flac), defaults to mp3
```

### Deploy to Sevalla

1.  Click the button below to deploy the bot to Sevalla.

    [![Deploy to Sevalla](https://www.sevalla.com/button.svg)](https://app.sevalla.com/apps/new/template?template=https://github.com/Mxx-x/Bluto)

2.  After clicking the button, you will be redirected to Sevalla to complete the deployment. You will need to:
    *   Connect your GitHub account.
    *   Choose a name for your application.
    *   Select a data center region.
    *   Configure the required environment variables as listed in the [Prerequisites](#prerequisites) section.
3.  You will also need to set up a PostgreSQL database on Sevalla and add the `DATABASE_URL` environment variable to your application.

### Deploy with Docker

1.  Clone the repository:
    ```bash
    git clone https://github.com/Mxx-x/Bluto.git
    cd Bluto
    ```
2.  Create a `.env` file with the configuration variables mentioned above.
3.  Build the Docker image:
    ```bash
    docker build -t bluto-music-bot .
    ```
4.  Run the Docker container:
    ```bash
    docker run -d --env-file .env --name bluto-music-bot bluto-music-bot
    ```

### Deploy without Docker

1.  Clone the repository:
    ```bash
    git clone https://github.com/Mxx-x/Bluto.git
    cd Bluto
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Create a `.env` file with the configuration variables.
4.  Run the bot:
    ```bash
    python -m Bluto
    ```

## Commands

### User Commands
- `/start`: Starts the bot and shows the main menu.
- `/play <song name or link>`: Plays a song from YouTube, Spotify, or YouTube Music.
- `/song <song name or link>`: Downloads a song. In groups with the feature enabled, it provides a private link to get the song.
- `/queue`: Shows the list of songs in the queue.

### Admin Commands
- `/playnow <song name or link>`: Plays a song immediately, without adding it to the queue.
- `/pause`: Pauses the music.
- `/resume`: Resumes the music.
- `/skip`: Skips the current song.
- `/end` or `/stop`: Stops the music and leaves the voice chat.
- `/clearqueue`: Clears the queue.
- `/shuffle`: Shuffles the queue.
- `/ban <user>`: Bans a user from using the bot.
- `/unban <user>`: Unbans a user.
- `/warn <user>`: Warns a user.
- `/songstatus <group_id>`: Enables or disables the advanced song download feature for a group.


## Credits

This project is inspired by and uses code from:
- [Yukki Music Bot](https://github.com/TeamYukki/YukkiMusicBot)
- [py-tgcalls](https://github.com/pytgcalls/pytgcalls)
