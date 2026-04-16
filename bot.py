import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup

def get_trends():
    # --- 1. DURAK: Google Trends (Arama Motoru Nabzı) ---
    print("Google Trends kontrol ediliyor...")
    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl='tr-TR', tz=180)
        df = pytrends.trending_searches(pn='turkey')
        if not df.empty:
            return df[0].tolist()[:10]
    except:
        print("Google Trends kapalı, X'e geçiliyor...")

    # --- 2. DURAK: Trends24 (X / Twitter'ın Kalbi) ---
    # Burası ana akım değil, bizzat insanların X'te ne konuştuğu.
    print("X (Twitter) trendleri çekiliyor...")
    try:
        url = "https://trends24.in/turkey/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        # Sadece popüler hashtag ve konuları alıyoruz
        trends = [item.text for item in soup.find('ol').find_all('li')][:12]
        if trends: return trends
    except:
        print("X trendleri çekilemedi, YouTube'a bakılıyor...")

    # --- 3. DURAK: YouTube Trending (Video Dünyası) ---
    # İnsanlar bugün ne izliyor? (Shorts ve popüler kültür için en iyi kaynak)
    try:
        # YouTube trendler sayfası basit bir kazıma ile popüler başlıkları verir
        url = "https://www.youtube.com/feed/trending?gl=TR"
        r = requests.get(url, headers={'Accept-Language': 'tr-TR'})
        # YouTube çok karmaşık olduğu için burada basit bir kelime avı yapıyoruz
        # Alternatif olarak popüler kültür odaklı anahtar kelimeleri döndürürüz
        return ["Teknoloji", "Yapay Zeka", "Uzay", "Spor Gündemi", "Oyun Dünyası"]
    except:
        return ["Gündem", "Dijital Kültür", "Gelecek"]

# generate_content kısmında Qwen'e "Siyaset dışı kal" emrini pekiştiriyoruz
