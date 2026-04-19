import requests
from bs4 import BeautifulSoup
import feedparser
import os

def fetch_rss_collection():
    """RSS üzerinden teknoloji, bilim ve yaşam haberlerini toplar."""
    rss_list = [
        "https://webrazzi.com/feed/", "https://shiftdelete.net/feed",
        "https://evrimagaci.org/rss.xml", "https://www.donanimhaber.com/rss/tum/",
        "https://pazarlamasyon.com/feed", "https://www.arkeofili.com/feed/",
        "https://t24.com.tr/rss/haber/bilim-teknoloji", "https://feeds.feedburner.com/Teknolojioku",
        "https://physicsworld.com/feed/", "https://www.wired.com/feed/rss"
    ]
    titles = []
    for url in rss_list:
        try:
            feed = feedparser.parse(url)
            titles.extend([entry.title for entry in feed.entries[:5]])
        except: continue
    return titles

def fetch_trends24():
    """X/Twitter gündemini daha derin kazır."""
    try:
        r = requests.get("https://trends24.in/turkey/", timeout=15)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        # Sadece ilk listeyi değil, tüm saatleri tara (havuzu büyütmek için)
        trends = [item.text.strip() for item in soup.find_all('li')]
        return trends[:50] 
    except: return []

def get_all_raw_data():
    print("🌐 Devasa veri havuzu toplanıyor...")
    # RSS + Trends + Google birleşiyor
    pool = fetch_rss_collection() + fetch_trends24()
    # Google Trends proxy hatası alıyorsa en azından diğerleri havuzu doldurur
    return list(dict.fromkeys(pool)) # Tekrarları sil
