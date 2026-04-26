import feedparser
from bs4 import BeautifulSoup

def fetch_rich_news():
    # Tüm kaynakları tek bir listede topluyoruz (Hata riskini sıfırlamak için)
    rss_list = [
        "https://webrazzi.com/feed/",
        "https://shiftdelete.net/feed",
        "https://www.donanimhaber.com/rss/tum/",
        "https://evrimagaci.org/rss.xml",
        "https://www.arkeofili.com/feed/",
        "https://pazarlamasyon.com/feed",
        "https://t24.com.tr/rss/haber/kultur-sanat",
        "https://www.teknolojioku.com/rss",
        "https://www.chip.com.tr/rss",
        "https://www.cumhuriyet.com.tr/rss/son_dakika.xml"
    ]
    
    rich_pool = []
    print(f"📡 {len(rss_list)} kaynaktan veri çekiliyor...")
    
    for url in rss_list:
        try:
            feed = feedparser.parse(url)
            # Her kaynaktan en güncel 8 haberi alıyoruz
            for entry in feed.entries[:8]:
                # Başlık ve özet birleştiriliyor
                summary_raw = getattr(entry, 'summary', '') or getattr(entry, 'description', '')
                clean_summary = BeautifulSoup(summary_raw, "html.parser").text[:400].strip()
                
                content_block = f"BAŞLIK: {entry.title} | DETAY: {clean_summary}"
                rich_pool.append(content_block)
        except Exception as e:
            print(f"⚠️ {url} adresinden veri çekilemedi: {e}")
            continue
            
    return rich_pool

def get_all_raw_data():
    data = fetch_rich_news()
    print(f"✅ Toplam {len(data)} haber bloğu havuzda toplandı.")
    return data
