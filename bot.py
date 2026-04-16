import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from filter_engine import clean_trends  # Filtre motorumuzu içeri alıyoruz

def fetch_trends24():
    """X (Twitter) trendlerini Trends24 üzerinden çeker."""
    try:
        url = "https://trends24.in/turkey/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        r = requests.get(url, headers=headers, timeout=15)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        return [item.text.strip() for item in soup.find('ol').find_all('li')]
    except Exception as e:
        print(f"Trends24 hatası: {e}")
        return []

def fetch_google_trends():
    """Google'da en çok arananları çeker."""
    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl='tr-TR', tz=180)
        df = pytrends.trending_searches(pn='turkey')
        return df[0].tolist() if not df.empty else []
    except Exception as e:
        print(f"Google Trends hatası: {e}")
        return []

def generate_content(trends):
    """Qwen 1.5b ile detoks ruhuna uygun içerik üretir."""
    date_str = datetime.now().strftime('%d.%m.%Y')
    
    prompt = f"""
    Sen @olanlarsakami editörüsün. Modern, ferah ve zeki bir tarzın var.
    Şu temizlenmiş gündem kelimelerini kullanarak günün özetini yaz: {trends}

    [KİMLİK VE ÜSLUP]
    - Siyasetten, dramdan ve kasvetten nefret edersin. 
    - İşin; insanlara 'Bugün şunlar oldu, kafan rahat olsun' dedirtmek.
    - Dilin samimi (kanka tarzı), kısa cümleli ve emojili olsun.

    [FORMAT]
    [X_THREAD]
    - 5 Tweetlik akış (Aralara '---' koy). 'Şaka mı bu?' enerjisiyle gir.
    
    [WEB_ARTICLE]
    - Başlık: {date_str} - Günün Ferah Özeti 🌿
    - 3-4 maddede, robotik olmayan, samimi bir dille günün analizini yap.
    """
    
    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "qwen2.5:1.5b",
                "prompt": prompt,
                "stream": False,
                "options": {"num_predict": 700, "temperature": 0.7}
            }, timeout=180)
        return response.json().get('response', 'AI içerik üretemedi.')
    except Exception as e:
        return f"Üretim hatası: {e}"

def save_to_txt(content):
    date_filename = datetime.now().strftime('%d_%m_%Y') + ".txt"
    with open(date_filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Dosya başarıyla kaydedildi: {date_filename}")

if __name__ == "__main__":
    print("Süreç başladı: Veri havuzu toplanıyor...")
    
    # Tüm kaynaklardan veri topla
    raw_pool = fetch_trends24() + fetch_google_trends()
    
    # Havuzu filtre motoruna gönder
    clean_pool = clean_trends(raw_pool)
    print(f"Filtre sonrası temiz gündem: {clean_pool}")
    
    if clean_pool:
        final_content = generate_content(clean_pool)
        save_to_txt(final_content)
        print("İşlem tamamlandı!")
    else:
        print("Hata: Filtre sonrası veri kalmadı.")
