-- Creating table for LLMConfig model with optimized constraints
CREATE TABLE IF NOT EXISTS llm_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    base_url TEXT NOT NULL DEFAULT 'https://api.openai.com/v1',
    model TEXT NOT NULL CHECK(model <> ''),
    api_key TEXT NOT NULL CHECK(api_key <> ''),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(base_url, model)
);

-- Creating index for llm_config queries
CREATE INDEX IF NOT EXISTS idx_llm_config_model ON llm_config(model);