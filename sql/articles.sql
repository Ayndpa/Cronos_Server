-- Creating table for Articles with optimized constraints and indexes
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    feed_id INTEGER NOT NULL,
    title TEXT NOT NULL CHECK(title <> ''),
    link TEXT NOT NULL CHECK(link <> ''),
    guid TEXT NOT NULL CHECK(guid <> '') UNIQUE,
    pub_date TEXT NOT NULL CHECK(pub_date <> ''),
    author TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (feed_id) REFERENCES rss_feeds(id) ON DELETE CASCADE
);

-- Creating indexes for articles queries
CREATE INDEX IF NOT EXISTS idx_articles_feed_id ON articles(feed_id);
CREATE INDEX IF NOT EXISTS idx_articles_guid ON articles(guid);
CREATE INDEX IF NOT EXISTS idx_articles_pub_date ON articles(pub_date);
