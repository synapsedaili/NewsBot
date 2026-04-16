import os
import requests
from datetime import datetime
from filter_engine import ai_clean_trends

# --- PROXY AYARLARI (Eğer elinde varsa buraya gir kanka) ---
# Format: "http://user:password@ip:port"
PROXIES = {
    "http": os.getenv("PROXY_URL"), # GitHub Secrets içine PROXY_URL eklersen daha güvenli olur
    "https": os.getenv("PROXY_URL")
}

def fetch_google_trends():
    """Google Trends verisini Proxy desteği ile çeker."""
    print("Google Trends çekiliyor (IP Değiştirme aktif)...")
    try:
        from pytrends.request import TrendReq
        
        # Proxy ayarlarını pytrends'e gömüyoruz
        pytrends = TrendReq(
            hl='tr-TR', 
            tz=180, 
            timeout=(10, 25), 
            proxies=[os.getenv("PROXY_URL")] if os.getenv("PROXY_URL") else None,
            retries=2,
            backoff_factor=0.5
        )
        
        df = pytrends.trending_searches(pn='turkey')
        if not df.empty:
            print("Google Trends başarıyla çekildi.")
            return df[0].tolist()
        return []
    except Exception as e:
        print(f"Google Trends çekilemedi: {e}")
        return []

def generate_content(trends):
    """Mistral 7B ile kaliteli içerik üretimi."""
    date_str = datetime.now().strftime('%d.%m.%Y')
    
    # Mistral için daha net ve karakter kısıtlamalı prompt
    prompt = f"""
    [SYSTEM]
    Sen @olanlarsakami editörüsün. Tarzın: Modern, zeki, ferah ve hafif ironik.
    Kullanacağın Gündem: {trends}

    [GÖREV]
    1. X_THREAD: 5 tweetlik akış. 'Şaka mı bu?' enerjisiyle başla. Tweetler arası '---' koy.
    2. WEB_ARTICLE: '{date_str} - Günün Ferah Özeti 🌿' başlığıyla, samimi ve kısa 3 madde.

    [KURAL]
    SADECE Türkçe cevap ver. Siyaset, dram ve robotik tekrarlardan kaçın.
    """
    
    print(f"Mistral 7B içerik üretiyor (Tarih: {date_str})...")
    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 1000,
                    "temperature": 0.75,
                    "top_p": 0.9
                }
            }, timeout=300)
        return response.json().get('response', 'Hata: AI içerik üretemedi.')
    except Exception as e:
        return f"Üretim hatası: {e}"

def save_to_txt(content):
    date_filename = datetime.now().strftime('%d_%m_%Y') + ".txt"
    with open(date_filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Başarılı: {date_filename} kaydedildi.")

if __name__ == "__main__":
    # 1. Ham veriyi çek
    raw_trends = fetch_google_trends()
    
    # 2. AI Filtreleme (AI'nın AI'yı denetlediği yer)
    # filter_engine içindeki ai_clean_trends fonksiyonunu Mistral'e bağladığından emin ol kanka!
    clean_pool = ai_clean_trends(raw_trends)
    print(f"Onaylanan Temiz Liste: {clean_pool}")
    
    # 3. İçerik Üretimi
    if clean_pool:
        final_content = generate_content(clean_pool)
        save_to_txt(final_content)
        print("Süreç tamamlandı.")
    else:
        print("Bugünlük temiz veri bulunamadı, sistem beklemede.")
