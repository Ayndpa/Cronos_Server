import sqlite3
from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import HttpUrl

from models.rss.feed import Feed
from services.database import get_db
from services.rss.feed import create_feed, delete_feed, get_all_feeds, get_feed_by_id, update_feed


# Create an APIRouter instance
router = APIRouter(
    prefix="/rss/feed",
    tags=["feeds"],
)

@router.get("/", response_model=List[Feed])
def read_feeds(db: sqlite3.Connection = Depends(get_db)):
    """
    Retrieve all RSS feeds.
    """
    return get_all_feeds(db)

@router.get("/{feed_id}", response_model=Feed)
def read_feed_by_id(feed_id: int, db: sqlite3.Connection = Depends(get_db)):
    """
    Retrieve a specific RSS feed by its ID.
    """
    feed = get_feed_by_id(db, feed_id)
    if not feed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feed not found",
        )
    return feed

@router.post("/", response_model=Feed, status_code=status.HTTP_201_CREATED)
def create_new_feed(feed: Feed, db: sqlite3.Connection = Depends(get_db)):
    """
    Create a new RSS feed.
    """
    return create_feed(db, name=feed.name, url=feed.url)

@router.put("/{feed_id}", response_model=Feed)
def update_existing_feed(
    feed_id: int, feed: Feed, db: sqlite3.Connection = Depends(get_db)
):
    """
    Update an existing RSS feed by its ID.
    """
    updated_feed = update_feed(db, feed_id, name=feed.name, url=feed.url)
    if not updated_feed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feed not found",
        )
    return updated_feed

@router.delete("/{feed_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_feed(feed_id: int, db: sqlite3.Connection = Depends(get_db)):
    """
    Delete an RSS feed by its ID.
    """
    if not delete_feed(db, feed_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feed not found",
        )
    return None