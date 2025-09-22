CREATE TABLE IF NOT EXISTS banned_users (
    user_id BIGINT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS song_download_settings (
    chat_id BIGINT PRIMARY KEY,
    enabled BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS song_requests (
    request_id TEXT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    query TEXT NOT NULL,
    chat_id BIGINT NOT NULL,
    message_id BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS queue (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    song_details JSONB NOT NULL,
    position INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS player_status (
    chat_id BIGINT PRIMARY KEY,
    status TEXT NOT NULL
);
