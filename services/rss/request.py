import feedparser
import requests
from typing import Optional

def get_rss_feed(url: str, timeout: int = 30) -> Optional[dict]:
    """
    从给定的URL获取并解析RSS或Atom订阅源。

    此函数使用 requests 库获取订阅源内容，然后使用 feedparser 库进行解析。
    它会处理常见的网络错误，并返回一个字典形式的解析结果。

    Args:
        url: 订阅源的URL字符串。
        timeout: 请求的超时时间（秒）。

    Returns:
        如果成功解析，返回一个包含订阅源数据的字典。
        如果发生错误（如网络问题、解析失败），则返回 None。
    """
    try:
        # 使用 requests 获取订阅源内容
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, timeout=timeout, headers=headers)
        response.raise_for_status()  # 如果状态码不是200，则抛出HTTPError

        # 使用 feedparser 解析内容
        feed = feedparser.parse(response.content)

        # 检查解析是否成功
        if feed.bozo:
            print(f"警告：无法完全解析此订阅源 ({url})。可能存在格式问题。")
            return None
        
        return feed

    except requests.exceptions.RequestException as e:
        print(f"请求RSS订阅源时发生错误：{e}")
        return None
    except Exception as e:
        print(f"解析RSS订阅源时发生意外错误：{e}")
        return None

# --- 示例用法 ---
if __name__ == '__main__':
    rss_url = "https://www.nasa.gov/rss/dyn/breaking_news.rss"
    
    print(f"正在尝试获取RSS订阅源：{rss_url}\n")
    
    feed_data = get_rss_feed(rss_url)
    
    if feed_data:
        # 打印订阅源标题
        print(f"订阅源标题: {feed_data.feed.title}")
        print(f"链接: {feed_data.feed.link}\n")
        
        # 打印最新的5篇文章
        print("最新5篇文章：")
        for entry in feed_data.entries[:5]:
            print("-" * 20)
            print(f"标题: {entry.title}")
            print(f"链接: {entry.link}")
            # 注意：某些RSS源可能没有'published'字段
            if 'published' in entry:
                print(f"发布日期: {entry.published}")
            print("\n")
    else:
        print("未能获取或解析RSS订阅源。")