CREATE TABLE IF NOT EXISTS posts (
    post_id TEXT PRIMARY KEY,
    post_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS candidates (
    candidate_id TEXT PRIMARY KEY,
    post_id text REFERENCES posts(post_id) ON DELETE CASCADE,
    candidate_name TEXT
);

CREATE TABLE IF NOT EXISTS authorized_users(
    id TEXT PRIMARY KEY
    identifier TEXT UNIQUE,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    invoker_id TEXT REFERENCES authorized_users(id),
    session_id TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS votes (
    session_id TEXT REFERENCES sessions(session_id) ON DELETE RESTRICT,
    votes TEXT NOT NULL
);
