CREATE TABLE IF NOT EXISTS posts (
    post_id TEXT PRIMARY KEY,
    post_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS candidates (
    candidate_id TEXT PRIMARY KEY,
    post_id text REFERENCES posts(post_id),
    candidate_name TEXT
)
