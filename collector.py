import requests
from bs4 import BeautifulSoup
import feedparser
import os

PROXY_URL = os.getenv("PROXY_URL")

def fetch_google_trends():
    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl='tr-TR', tz=180, proxies=[PROXY_URL] if PROXY_URL else None)
        df = pytrends.trending_searches(pn='turkey')
        return df[0].tolist() if not df.empty else []
    except: return []

def fetch_trends24():
    try:
        r = requests.get("https://trends24.in/turkey/", timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        return [item.text.strip() for item in soup.find('ol').find_all('li')]
    except: return []

def fetch_rss_news():
    rss_urls = [
        "https://webrazzi.com/feed/", 
        "https://www.arkeofili.com/feed/",
        "https://evrimagaci.org/rss.xml"
    ]
    titles = []
    for url in rss_urls:
        try:
            feed = feedparser.parse(url)
            titles.extend([entry.title for entry in feed.entries[:5]])
        except: continue
    return titles

def get_all_raw_data():
    print("🌐 Veriler toplanıyor...")
    pool = fetch_google_trends() + fetch_trends24() + fetch_rss_news()
    return list(set(pool))
