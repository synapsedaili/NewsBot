import feedparser
from bs4 import BeautifulSoup

def fetch_rich_news():
    """Haber havuzunu devleştiren genişletilmiş kaynak listesi."""
    rss_sources = {
        "Teknoloji": [
            "https://webrazzi.com/feed/", 
            "https://shiftdelete.net/feed",
            "https://www.donanimhaber.com/rss/tum/"
        ],
        "Yerel & Genel (Yaşam Odaklı)": [
            "https://www.aa.com.tr/tr/rss/default?cat=yasam", # AA Yaşam Haberleri
            "https://www.aa.com.tr/tr/rss/default?cat=kultur", # AA Kültür
            "https://t24.com.tr/rss/haber/yasam"
        ],
        "Spor": [
            "https://www.fotomac.com.tr/rss/anasayfa.xml",
            "https://www.aspor.com.tr/rss/anasayfa.xml"
        ],
        "Bilim & Kültür": [
            "https://evrimagaci.org/rss.xml",
            "https://www.arkeofili.com/feed/",
            "https://popsci.com.tr/feed/"
        ],
        "Yaşam & Trend": [
            "https://listelist.com/feed/",
            "https://onedio.com/support/rss?category=4f311f93f1807d890e00000a" # Onedio Yaşam
        ]
    }
    
    rich_pool = []
    
    for category, urls in rss_sources.items():
        for url in urls:
            try:
                feed = feedparser.parse(url)
                # Her kaynaktan en güncel 5 haberi alıyoruz
                for entry in feed.entries[:5]:
                    # Bazı RSS'lerde summary olmayabilir, description kontrolü yapıyoruz
                    summary_raw = getattr(entry, 'summary', getattr(entry, 'description', ''))
                    clean_summary = BeautifulSoup(summary_raw, "html.parser").text[:400]
                    
                    content_block = f"KATEGORİ: {category} | BAŞLIK: {entry.title} | ÖZET: {clean_summary}"
                    rich_pool.append(content_block)
            except Exception as e:
                print(f"Hata: {url} kaynağından veri çekilemedi. {e}")
                continue
                
    return rich_pool

def get_all_raw_data():
    print(f"📡 Toplam {len(fetch_rich_news())} farklı haber bloğu toplanıyor...")
    return fetch_rich_news()
