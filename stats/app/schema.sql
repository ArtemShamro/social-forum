CREATE TABLE IF NOT EXISTS stats_db.events
(
    event_type String,
    post_id Int64,
    user_id String,
    comment_id Nullable(Int64),
    timestamp DateTime
)
ENGINE = MergeTree()
ORDER BY (timestamp, post_id, event_type);