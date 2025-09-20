# Bluto Music Bot

A Telegram VC Music Bot to play music in your group's voice chat.

## Features

- **Play from YouTube, Spotify, and YouTube Music:** Play any song from YouTube, Spotify, or YouTube Music by providing a link or by searching for the song name.
- **Queue System:** Add multiple songs to a queue. The bot will automatically play the next song when the current one finishes.
- **Inline Player Controls:** Pause, resume, skip, and stop the music using inline buttons.
- **Admin Controls:** Admins can play music directly, stop playback, ban/unban users, and warn users.
- **"Now Playing" Thumbnail:** The bot sends a beautiful thumbnail with the song details when a song starts playing.
- **Force Subscribe:** Require users to join a channel before using the bot in private messages.
- **Logging:** Log all music playback and admin actions to a designated log channel.
- **Docker Support:** Easy to deploy using Docker.

## Deployment

### Prerequisites

1.  **API_ID and API_HASH:** Get these from [my.telegram.org](https://my.telegram.org).
2.  **BOT_TOKEN:** Get this from [@BotFather](https://t.me/BotFather) on Telegram.
3.  **MONGO_DB_URI:** A MongoDB database URI. You can get one from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
4.  **OWNER_ID:** Your Telegram user ID. Get it from [@FallenIdsBot](https://t.me/FallenIdsBot).
5.  **LOG_GROUP_ID:** A private group ID for the bot to send logs.
6.  **FORCE_SUB_CHANNEL:** The username of the channel that users must join to use the bot (optional).

### Configuration

Create a `.env` file with the following variables:

```
API_ID=
API_HASH=
BOT_TOKEN=
MONGO_DB_URI=
OWNER_ID=
LOG_GROUP_ID=
SUDO_USERS=
BOT_USERNAME= # Your bot's username without the @
SUPPORT_CHANNEL= # Your support channel link
SUPPORT_GROUP= # Your support group link
FORCE_SUB_CHANNEL= # The username of the force subscribe channel (without the @)
```

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


## Credits

This project is inspired by and uses code from:
- [Yukki Music Bot](https://github.com/TeamYukki/YukkiMusicBot)
- [py-tgcalls](https://github.com/pytgcalls/pytgcalls)
