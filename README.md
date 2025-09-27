# Bluto Music Bot

A Telegram VC Music Bot to play music in your group's voice chat.

## Features

- **Play from YouTube, Spotify, and YouTube Music:** Play any song from YouTube, Spotify, or YouTube Music by providing a link or by searching for the song name.
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

### Deploy to Choreo

Choreo does not offer a one-click deploy button, but you can deploy the bot by following these manual steps:

1.  **Sign up for Choreo:** Create an account on the [Choreo website](https://console.choreo.dev/).
2.  **Create a Project:** Once you are logged in, create a new project.
3.  **Create a Component:**
    *   Inside your project, click on **Components** and then **Create**.
    *   Select **Service** as the component type.
    *   Choose **Deploy a containerized application** and click **Create**.
4.  **Connect to GitHub:**
    *   Connect your GitHub account to Choreo.
    *   Select this repository (`Mxx-x/Bluto`) to deploy.
5.  **Configure Build Settings:**
    *   Set the **Build Preset** to **Dockerfile**.
    *   Ensure the **Dockerfile Path** is set to `./Dockerfile`.
    *   Click **Create**.
6.  **Create a PostgreSQL Database:**
    *   Navigate to the **Dependencies** tab within your project.
    *   Click on **Create** and select **PostgreSQL** from the list of managed databases.
    *   Follow the prompts to create the database.
7.  **Connect the Database:**
    *   Once the database is created, go to the **Settings** of your service component.
    *   Under **Dependencies**, click on **Add** and select the PostgreSQL database you just created.
    *   This will automatically add the `DATABASE_URL` to your environment variables.
8.  **Configure Environment Variables:**
    *   In your service's **Settings**, go to the **Environment Variables** section.
    *   Add all the other required environment variables as listed in the [Prerequisites](#prerequisites) section.
9.  **Deploy:**
    *   Go to the **Deploy** tab of your service.
    *   Click on **Deploy** to build and deploy the bot.

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

### Run with GitHub Actions (for testing)

This method is not recommended for hosting the bot 24/7 due to GitHub Actions' execution time limits. However, it can be useful for testing or short-term use.

1.  **Fork this repository:** Click the **Fork** button at the top right of this page to create your own copy of the repository.
2.  **Create a PostgreSQL Database:** You will need a publicly accessible PostgreSQL database. You can get a free one from services like [Neon](https://neon.tech/) or [Supabase](https://supabase.com/).
3.  **Set up Repository Secrets:**
    *   In your forked repository, go to **Settings** > **Secrets and variables** > **Actions**.
    *   Click on **New repository secret** for each of the environment variables listed in the [Prerequisites](#prerequisites) section.
    *   Make sure to include your `DATABASE_URL` from the database you created.
4.  **Run the Workflow:**
    *   Go to the **Actions** tab of your forked repository.
    *   Select the **Run Bluto Music Bot (Manual)** workflow from the sidebar.
    *   Click on **Run workflow** and then **Run workflow** again to start the bot.
    *   The bot will run until the workflow is stopped or reaches its time limit (up to 6 hours).

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
