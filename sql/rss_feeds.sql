-- Creating table for RSS feeds with optimized constraints
CREATE TABLE IF NOT EXISTS rss_feeds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL CHECK(name <> ''),
    url TEXT NOT NULL CHECK(url <> '') UNIQUE,
    is_active BOOLEAN NOT NULL DEFAULT 1
);

-- Creating index for rss_feeds queries
CREATE INDEX IF NOT EXISTS idx_rss_feeds_url ON rss_feeds(url);
