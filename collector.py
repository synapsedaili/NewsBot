import requests
import feedparser
from bs4 import BeautifulSoup
from gnews import GNews

def fetch_rss_news():
    """Genişletilmiş RSS Havuzu"""
    rss_list = [
        "https://webrazzi.com/feed/",
        "https://www.donanimhaber.com/rss/tum/",
        "https://evrimagaci.org/rss.xml",
        "https://www.arkeofili.com/feed/",
        "https://t24.com.tr/rss/haber/kultur-sanat",
        "https://www.cumhuriyet.com.tr/rss/son_dakika.xml"
    ]
    pool = []
    for url in rss_list:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                summary = BeautifulSoup(getattr(entry, 'summary', ''), "html.parser").text[:300]
                pool.append(f"[RSS] {entry.title} | {summary}")
        except: continue
    return pool

def fetch_hackernews():
    """Küresel Teknoloji ve Vizyon Gündemi"""
    pool = []
    try:
        response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10).json()
        for story_id in response[:5]:
            story = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json", timeout=10).json()
            if story: pool.append(f"[HN] {story.get('title')} | Küresel Vizyon Tartışması")
    except: pass
    return pool

def fetch_gnews():
    """Google News - Gerçek ve Filtresiz Gündem"""
    pool = []
    try:
        google_news = GNews(language='tr', country='TR', max_results=10)
        news = google_news.get_top_news()
        for item in news:
            pool.append(f"[GNews] {item.get('title')} | {item.get('description')}")
    except: pass
    return pool

def get_all_raw_data():
    print("🚀 Veri havuzu genişletiliyor...")
    return fetch_rss_news() + fetch_hackernews() + fetch_gnews()
