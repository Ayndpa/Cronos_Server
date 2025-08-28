from fastapi import APIRouter, Depends, HTTPException
from services.rss.article.state import (
    get_all_tags,
    get_today_update_count,
    mark_article_as_read,
)
from models.rss.article import ArticleState
from services.database import get_db
import sqlite3
from typing import List
from collections import Counter
from datetime import datetime

router = APIRouter(
    prefix="/rss/article/state",
    tags=["article_state"],
)

@router.get("/today-update-count", response_model=int)
def get_today_update_count_endpoint(db: sqlite3.Connection = Depends(get_db)):
    """
    获取今日更新的文章状态数量。
    """
    return get_today_update_count(db)

@router.get("/tags", response_model=List[dict])
def get_tags_with_count(db: sqlite3.Connection = Depends(get_db)):
    """
    获取所有文章状态中的唯一标签及其计数。
    """
    tags = get_all_tags(db)
    tag_counts = Counter(tags)
    return [{"name": tag, "count": count} for tag, count in tag_counts.items()]

@router.post("/mark-as-read/{article_id}", response_model=bool)
def mark_article_as_read_endpoint(article_id: int, db: sqlite3.Connection = Depends(get_db)):
    """
    标记指定文章为已读。
    """

    try:
        return mark_article_as_read(db, article_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))