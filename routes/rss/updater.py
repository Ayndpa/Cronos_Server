from fastapi import APIRouter, HTTPException
from threading import Thread
from services.rss.updater import RSSUpdater
from services.database import get_db
from services.rss.feed import get_feed_by_id

router = APIRouter(
    prefix="/rss/updater",
    tags=["RSS Updater"]
)
updater = RSSUpdater()
updater_thread = None

@router.post("/start")
def start_updater():
    global updater_thread
    if updater.running:
        raise HTTPException(status_code=400, detail="RSS 更新程序已在运行。")
    updater.running = True
    updater_thread = Thread(target=updater.start, daemon=True)
    updater_thread.start()
    return {"message": "RSS 更新程序已启动。"}

@router.post("/stop")
def stop_updater():
    if not updater.running:
        raise HTTPException(status_code=400, detail="RSS 更新程序未在运行。")
    updater.stop()
    return {"message": "RSS 更新程序已停止。"}

@router.get("/status")
def get_status():
    return {"running": updater.running}

@router.post("/refresh/all")
def refresh_all_feeds():
    if not updater.running:
        raise HTTPException(status_code=400, detail="RSS 更新程序未在运行。")
    updater.refresh_now()
    return {"message": "已立即刷新所有 RSS 源。"}

@router.post("/refresh/{feed_id}")
def refresh_feed(feed_id: int):
    db_generator = get_db()
    try:
        conn = next(db_generator)
        feed = get_feed_by_id(conn, feed_id)
        if not feed:
            raise HTTPException(status_code=404, detail=f"未找到 ID 为 {feed_id} 的 RSS 源。")
        updater.process_feed(conn, feed)
        return {"message": f"已立即刷新 RSS 源 (id: {feed_id})。"}
    except StopIteration:
        raise HTTPException(status_code=500, detail="数据库连接失败。")
    finally:
        updater.safely_close_generator(db_generator)