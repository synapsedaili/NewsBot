import feedparser
import requests
from bs4 import BeautifulSoup

def fetch_rich_news():
    """RSS üzerinden haber başlığı + minik özetini toplar."""
    rss_list = [
        "https://webrazzi.com/feed/", "https://shiftdelete.net/feed",
        "https://evrimagaci.org/rss.xml", "https://www.donanimhaber.com/rss/tum/",
        "https://www.arkeofili.com/feed/"
    ]
    rich_pool = []
    for url in rss_list:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                # Başlık ve özeti birleştirip AI'ya bağlam veriyoruz
                clean_summary = BeautifulSoup(entry.summary, "html.parser").text[:300]
                content_block = f"BAŞLIK: {entry.title} | ÖZET: {clean_summary}"
                rich_pool.append(content_block)
        except: continue
    return rich_pool

def get_all_raw_data():
    print("🌐 İçerikli veri havuzu toplanıyor...")
    # Sadece başlık değil, içerikli blokları döndürüyoruz
    return fetch_rich_news()
