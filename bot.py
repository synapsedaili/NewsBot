import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup

def get_trends():
    """Yedekli trend çekme motoru: Google -> Trends24 -> Fallback"""
    print("Trendler kontrol ediliyor...")
    
    # 1. Deneme: Google Trends
    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl='tr-TR', tz=180)
        df = pytrends.trending_searches(pn='turkey')
        if not df.empty:
            print("Google Trends verisi alındı.")
            return df[0].tolist()[:10]
    except Exception as e:
        print(f"Google Trends pas geçildi: {e}")

    # 2. Deneme: Trends24 (X / Twitter'ın Nabzı)
    try:
        url = "https://trends24.in/turkey/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers, timeout=15)
        r.encoding = 'utf-8' # Karakter hatasını önlemek için
        soup = BeautifulSoup(r.text, 'html.parser')
        trends = [item.text.strip() for item in soup.find('ol').find_all('li')][:12]
        if trends:
            print("X (Trends24) verisi alındı.")
            return trends
    except Exception as e:
        print(f"X trendleri pas geçildi: {e}")

    # Fallback: Eğer her şey patlarsa genel başlıklar
    return ["Teknoloji", "Yapay Zeka", "Bilim", "Uzay", "Spor Gündemi", "Dijital Yaşam"]

def generate_content(trends):
    """Qwen 1.5b ile ferah içerik üretimi"""
    date_str = datetime.now().strftime('%d.%m.%Y')
    
    # AI'yı hizaya getiren, karakter hatasını düzelttiren prompt
    prompt = f"""
    Sen @olanlarsakami hesabının zeki, modern ve samimi editörüsün. 
    Görevin: Aşağıdaki karmaşık trendleri süzüp ferah bir günlük özet hazırlamak.

    Günün Trendleri: {trends}

    [KURALLAR]
    - Dilin samimi (kanka tarzı), kısa ve öz olsun.
    - Siyasetin boğuculuğundan uzak dur, teknoloji, spor ve yaşam odaklı ol.
    - Karakter hataları varsa (tuhaf semboller gibi) onları düzeltip temiz Türkçe yaz.

    [FORMAT - BU ŞABLONA UY]
    [X_THREAD]
    - 5 Tweetlik akış. 'Şaka mı bu?' enerjisiyle başla.
    - Her tweet emoji içermeli ve kısa olmalı.
    - Tweetler arasında '---' kullan.

    [WEB_ARTICLE]
    - Başlık: {date_str} - Bugün Neler Oldu? 🌿
    - Robotik olma, arkadaşına anlatır gibi yaz. 
    - 3-4 maddede günün 'ferah' özetini geç.
    """
    
    print("İçerik AI (Qwen 1.5b) tarafından üretiliyor...")
    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "qwen2.5:1.5b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 600,
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }, timeout=180)
        
        if response.status_code == 200:
            content = response.json().get('response', '')
            return content
        else:
            return "Hata: AI yanıt vermedi."
    except Exception as e:
        return f"Bağlantı hatası: {e}"

def save_to_txt(content):
    """Dosyayı UTF-8 olarak kaydetme"""
    date_filename = datetime.now().strftime('%d_%m_%Y') + ".txt"
    try:
        with open(date_filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Başarılı: {date_filename} oluşturuldu.")
    except Exception as e:
        print(f"Dosya kaydetme hatası: {e}")

if __name__ == "__main__":
    print("Süreç başladı...")
    trends = get_trends()
    print(f"Çekilen Trendler: {trends}")
    
    full_content = generate_content(trends)
    save_to_txt(full_content)
    print("Süreç başarıyla tamamlandı.")
