-- Creating table for Config model
CREATE TABLE IF NOT EXISTS config (
    key TEXT PRIMARY KEY CHECK(key <> ''),
    value TEXT
);

-- Creating index for config queries
CREATE INDEX IF NOT EXISTS idx_config_key ON config(key);

-- Adding entry for RSS read interval (default 60 minutes)
INSERT OR IGNORE INTO config (key, value) VALUES ('rss_read_interval', '60');
-- Adding entry for enabling/disabling RSS auto-refresh (default 'true')
INSERT OR IGNORE INTO config (key, value) VALUES ('rss_auto_refresh', 'true');

-- LLM configuration
-- Adding entry for LLM configuration ID (default NULL)
INSERT OR IGNORE INTO config (key, value) VALUES ('llm_config_id', NULL);