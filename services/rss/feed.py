import sqlite3
from typing import List, Optional

from fastapi import HTTPException
from pydantic import HttpUrl

from models.rss.feed import Feed

def get_all_feeds(db: sqlite3.Connection) -> List[Feed]:
    """
    从数据库中检索所有 Feed。
    """
    try:
        cursor = db.cursor()
        cursor.execute("SELECT id, name, url, is_active FROM rss_feeds")
        feeds = cursor.fetchall()
        return [Feed(**feed) for feed in feeds]
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"获取所有 Feed 失败: {e}")

def get_feed_by_id(db: sqlite3.Connection, feed_id: int) -> Optional[Feed]:
    """
    根据 ID 检索单个 Feed。
    """
    try:
        cursor = db.cursor()
        cursor.execute("SELECT id, name, url, is_active FROM rss_feeds WHERE id = ?", (feed_id,))
        feed = cursor.fetchone()
        if feed:
            return Feed(**feed)
        return None
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"根据 ID 获取 Feed 失败: {e}")

def create_feed(db: sqlite3.Connection, name: str, url: HttpUrl) -> Optional[Feed]:
    """
    在数据库中创建一个新的 Feed。
    """
    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO rss_feeds (name, url, is_active) VALUES (?, ?, ?)",
            (name, str(url), True),
        )
        db.commit()
        feed_id = cursor.lastrowid
        return get_feed_by_id(db, feed_id)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="该 URL 的 Feed 已存在。")
    except sqlite3.Error as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建 Feed 失败: {e}")

def update_feed(db: sqlite3.Connection, feed_id: int, name: str, url: HttpUrl, is_active: bool = True) -> Optional[Feed]:
    """
    更新一个现有的 Feed。
    """
    try:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE rss_feeds SET name = ?, url = ?, is_active = ? WHERE id = ?",
            (name, str(url), is_active, feed_id),
        )
        db.commit()
        if cursor.rowcount == 0:
            return None  # 未找到 Feed
        return get_feed_by_id(db, feed_id)
    except sqlite3.Error as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新 Feed 失败: {e}")

def delete_feed(db: sqlite3.Connection, feed_id: int) -> bool:
    """
    根据 ID 删除一个 Feed。
    """
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM rss_feeds WHERE id = ?", (feed_id,))
        db.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除 Feed 失败: {e}")