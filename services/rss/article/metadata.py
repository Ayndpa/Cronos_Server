import sqlite3
from typing import List
from fastapi import HTTPException
from models.rss.article import Article

def article_exists(conn: sqlite3.Connection, guid: str) -> bool:
    """
    检查具有给定 GUID 的文章是否已存在。
    :param conn: 数据库连接实例。
    :param guid: 文章的唯一标识符。
    :return: 如果文章存在则返回 True，否则返回 False。
    """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM articles WHERE guid = ?", (guid,))
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        print(f"检查文章是否存在时出错: {e}")
        raise HTTPException(status_code=500, detail="数据库操作失败")