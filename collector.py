import requests
import feedparser
from bs4 import BeautifulSoup
from gnews import GNews

def fetch_rss_news():
    """Genişletilmiş RSS Kütüphanesi (ALL-about-RSS esintili)"""
    rss_list = [
        "https://webrazzi.com/feed/",
        "https://www.donanimhaber.com/rss/tum/",
        "https://evrimagaci.org/rss.xml",
        "https://www.arkeofili.com/feed/",
        "https://t24.com.tr/rss/haber/kultur-sanat",
        "https://www.cumhuriyet.com.tr/rss/son_dakika.xml"
    ]
    pool = []
    print("📡 RSS kaynakları taranıyor...")
    for url in rss_list:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                summary_raw = getattr(entry, 'summary', '') or getattr(entry, 'description', '')
                clean_summary = BeautifulSoup(summary_raw, "html.parser").text[:300].strip()
                pool.append(f"[RSS] BAŞLIK: {entry.title} | ÖZET: {clean_summary}")
        except: continue
    return pool

def fetch_hackernews():
    """Küresel vizyon ve teknoloji felsefesi gündemi"""
    pool = []
    print("🌍 HackerNews küresel gündemi çekiliyor...")
    try:
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(url, timeout=10).json()
        # En popüler 5 tartışmayı al
        for story_id in response[:5]:
            story = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json", timeout=10).json()
            if story and 'title' in story:
                pool.append(f"[HN] BAŞLIK: {story['title']} | ÖZET: Küresel teknoloji ve vizyon tartışması.")
    except Exception as e:
        print(f"⚠️ HackerNews Hatası: {e}")
    return pool

def fetch_gnews():
    """Google News üzerinden filtresiz gerçek dünya gündemi"""
    pool = []
    print("📰 GNews ile yerel/global gerçek gündem taranıyor...")
    try:
        google_news = GNews(language='tr', country='TR', max_results=10)
        # Sadece teknoloji değil, 'Top News' yani ana gündemi alıyoruz
        news = google_news.get_top_news()
        for item in news:
            title = item.get('title', '')
            desc = item.get('description', '')
            pool.append(f"[GNews] BAŞLIK: {title} | ÖZET: {desc}")
    except Exception as e:
        print(f"⚠️ GNews Hatası: {e}")
    return pool

def get_all_raw_data():
    """Tüm motorları çalıştırıp devasa havuzu oluşturur"""
    print("🚀 Veri İstasyonu Aktif: Çoklu kaynak entegrasyonu başlatıldı...")
    data = fetch_rss_news() + fetch_hackernews() + fetch_gnews()
    print(f"✅ İşlem Tamam! Toplam {len(data)} adet taze haber bloğu filtreye gitmeye hazır.")
    return data
