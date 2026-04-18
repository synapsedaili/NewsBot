import requests
from bs4 import BeautifulSoup
import feedparser
import os

def fetch_google_trends():
    try:
        from pytrends.request import TrendReq
        # Proxy varsa secrets'tan çeker
        proxy = os.getenv("PROXY_URL")
        pytrends = TrendReq(hl='tr-TR', tz=180, proxies=[proxy] if proxy else None)
        df = pytrends.trending_searches(pn='turkey')
        return df[0].tolist() if not df.empty else []
    except: return []

def fetch_trends24():
    try:
        r = requests.get("https://trends24.in/turkey/", timeout=15)
        r.encoding = r.apparent_encoding # Karakter hatasını önleyen kritik dokunuş
        soup = BeautifulSoup(r.text, 'html.parser')
        return [item.text.strip() for item in soup.find('ol').find_all('li')]
    except: return []

def fetch_rss_news():
    rss_urls = [
        "https://webrazzi.com/feed/", 
        "https://www.arkeofili.com/feed/",
        "https://evrimagaci.org/rss.xml",
        "https://shiftdelete.net/feed"
    ]
    titles = []
    for url in rss_urls:
        try:
            feed = feedparser.parse(url)
            titles.extend([entry.title for entry in feed.entries[:5]])
        except: continue
    return titles

def get_all_raw_data():
    print("🌐 Tüm kaynaklardan ham veri havuzu oluşturuluyor...")
    pool = fetch_google_trends() + fetch_trends24() + fetch_rss_news()
    return list(set(pool))
