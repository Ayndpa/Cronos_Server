from sqlite3 import Connection
from typing import List, Optional
from models.config import Config

def create_config(db: Connection, key: str, value: str) -> Config:
    """
    Create a new config entry.
    """
    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO config (key, value) VALUES (?, ?)",
            (key, value),
        )
        db.commit()
        return Config(key=key, value=value)
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to create config: {e}")

def get_config(db: Connection, key: str) -> Optional[Config]:
    """
    Retrieve a config entry by key.
    """
    cursor = db.cursor()
    cursor.execute("SELECT key, value FROM config WHERE key = ?", (key,))
    row = cursor.fetchone()
    if row:
        return Config(key=row["key"], value=row["value"])
    return None

def update_config(db: Connection, key: str, value: str) -> Config:
    """
    Update an existing config entry.
    """
    try:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE config SET value = ? WHERE key = ?",
            (value, key),
        )
        if cursor.rowcount == 0:
            raise ValueError(f"Config with key '{key}' does not exist.")
        db.commit()
        return Config(key=key, value=value)
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to update config: {e}")

def delete_config(db: Connection, key: str) -> None:
    """
    Delete a config entry by key.
    """
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM config WHERE key = ?", (key,))
        if cursor.rowcount == 0:
            raise ValueError(f"Config with key '{key}' does not exist.")
        db.commit()
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to delete config: {e}")

def list_configs(db: Connection) -> List[Config]:
    """
    List all config entries.
    """
    cursor = db.cursor()
    cursor.execute("SELECT key, value FROM config")
    rows = cursor.fetchall()
    return [Config(key=row["key"], value=row["value"]) for row in rows]