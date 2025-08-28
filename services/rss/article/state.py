from datetime import datetime
from typing import List
from fastapi import HTTPException
import sqlite3

def get_all_tags(db: sqlite3.Connection) -> List[str]:
    """
    获取所有文章状态中的唯一标签。
    """
    try:
        cursor = db.cursor()
        cursor.execute("SELECT tags FROM article_states")
        rows = cursor.fetchall()
        tags = set()
        for row in rows:
            if row["tags"]:
                tags.update(row["tags"].split(","))
        return list(tags)
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"数据库错误: {e}")
    
def get_today_update_count(db: sqlite3.Connection) -> int:
    """
    获取今日更新的文章状态数量。
    """
    try:
        cursor = db.cursor()
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            """
            SELECT COUNT(*) as count
            FROM article_states
            WHERE DATE(updated_at) = ?
            """,
            (today,),
        )
        row = cursor.fetchone()
        return row["count"] if row else 0
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"数据库错误: {e}")
    
def mark_article_as_read(db: sqlite3.Connection, article_id: int) -> None:
    """
    将指定文章标记为已读。
    """
    try:
        cursor = db.cursor()
        cursor.execute(
            """
            UPDATE article_states
            SET is_read = 1, updated_at = ?
            WHERE id = ?
            """,
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), article_id),
        )
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="文章未找到")
        else:
            return True
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"数据库错误: {e}")
    
def save_ai_summary(db: sqlite3.Connection, article_id: int, ai_summary: str) -> None:
    """
    保存AI生成的总结信息到指定文章状态。
    """
    try:
        cursor = db.cursor()
        cursor.execute(
            """
            UPDATE article_states
            SET ai_summary = ?, updated_at = ?
            WHERE id = ?
            """,
            (ai_summary, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), article_id),
        )
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="文章未找到")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"数据库错误: {e}")
    
def get_ai_summary(db: sqlite3.Connection, article_id: int) -> str:
    """
    获取指定文章的AI生成总结信息。
    """
    try:
        cursor = db.cursor()
        cursor.execute(
            """
            SELECT ai_summary
            FROM article_states
            WHERE id = ?
            """,
            (article_id,),
        )
        row = cursor.fetchone()
        if row and row["ai_summary"]:
            return row["ai_summary"]
        else:
            return None
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"数据库错误: {e}")