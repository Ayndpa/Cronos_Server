# services/playwright.py
from playwright.async_api import async_playwright
from typing import Tuple

async def startup_playwright() -> Tuple[object, object]:
    """
    启动 Playwright 并返回 (pw, browser)。
    在 FastAPI 的 lifespan 中调用。
    """
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(headless=True)
    return pw, browser

async def shutdown_playwright(pw, browser) -> None:
    """
    关闭 browser 和 playwright。
    """
    try:
        if browser:
            await browser.close()
    finally:
        if pw:
            await pw.stop()

async def scrape_article(browser, url: str, timeout: int = 60000) -> str:
    """
    使用传入的 browser 实例抓取页面纯文本。
    每次用 new_context() 保持会话隔离，结束时关闭 context/page。
    """
    context = await browser.new_context()
    page = await context.new_page()
    try:
        await page.goto(url, timeout=timeout)
        await page.wait_for_load_state("networkidle")
        content = await page.inner_text("body")
        return content
    finally:
        # 尽量确保资源释放，不抛出二次异常遮蔽原错误
        try:
            await page.close()
        except Exception:
            pass
        try:
            await context.close()
        except Exception:
            pass
