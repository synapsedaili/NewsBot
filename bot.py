import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup

# --- AYARLAR ---
MODEL_NAME = "mistral"
OLLAMA_URL = "http://localhost:11434/api/generate"

def fetch_raw_trends():
    """Tüm dijital kaynaklardan ham veriyi toplar."""
    print("Trend havuzu toplanıyor...")
    trends = []
    
    # 1. Kaynak: Trends24 (X Gündemi)
    try:
        url = "https://trends24.in/turkey/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers, timeout=15)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        trends.extend([item.text.strip() for item in soup.find('ol').find_all('li')])
    except Exception as e:
        print(f"X verisi çekilemedi: {e}")

    # 2. Kaynak: Google Trends
    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl='tr-TR', tz=180)
        df = pytrends.trending_searches(pn='turkey')
        if not df.empty:
            trends.extend(df[0].tolist())
    except Exception as e:
        print(f"Google Trends verisi çekilemedi: {e}")

    return list(dict.fromkeys(trends)) # Tekrar edenleri temizle

def ai_filter_trends(raw_list):
    """Mistral 7B'yi kullanarak trendleri 'Detoks' süzgecinden geçirir."""
    print(f"Mistral {len(raw_list)} adet trendi analiz ediyor...")
    
    filter_prompt = f"""
    Sen bir editörsün. Aşağıdaki trend listesini 'Dijital Detoks' konseptine göre ele.
    
    KRİTERLER:
    1. Siyaset, tarikat, dini tartışmalar ve politik isimleri (Erdoğan, AKP, CHP vb.) ASLA SEÇME.
    2. Bot saldırılarını, anlamsız hashtagleri (c31k, furkan, vb.) ELE.
    3. Ölüm, cinayet, ağır dram içeren kasvetli haberleri ELE.
    4. SADECE Teknoloji, Spor, Bilim, Uzay ve Pozitif Yaşam olaylarını SEÇ.
    
    TREND LİSTESİ: {raw_list}
    
    ÇIKTI: Sadece seçtiğin 5-6 adet temiz trendi aralarına virgül koyarak yaz. Başka hiçbir şey yazma.
    """
    
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME,
            "prompt": filter_prompt,
            "stream": False,
            "options": {"temperature": 0.1}
        }, timeout=120)
        return response.json().get('response', '').split(',')
    except:
        return raw_list[:5] # Hata olursa güvenli bölgeye kaç

def generate_content(clean_trends):
    """Mistral 7B ile ferah içerik üretimi."""
    date_str = datetime.now().strftime('%d.%m.%Y')
    
    main_prompt = f"""
    Sen @olanlarsakami editörüsün. Modern, ferah ve ironik bir tarzın var.
    Şu temizlenmiş gündemi kullanarak günün özetini yaz: {clean_trends}

    [KİMLİK VE ÜSLUP]
    - Siyasetten ve dramdan uzak dur.
    - Samimi, 'kanka' tarzında, kısa ve öz cümleler kur.
    - Amacın okuyucuyu boğmak değil, ferahlatmak.

    [FORMAT]
    [X_THREAD]
    - 5 Tweetlik akış (Aralara '---' koy). 'Şaka mı bu?' enerjisiyle başla.
    
    [WEB_ARTICLE]
    - Başlık: {date_str} - Günün Ferah Özeti 🌿
    - 3 kısa maddede günün 'ferah' analizini yap.
    """
    
    print("Mistral içerik üretiyor...")
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME,
            "prompt": main_prompt,
            "stream": False,
            "options": {"temperature": 0.7, "num_predict": 800}
        }, timeout=240)
        return response.json().get('response', '')
    except Exception as e:
        return f"İçerik üretim hatası: {e}"

def save_to_txt(content):
    filename = datetime.now().strftime('%d_%m_%Y') + ".txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Başarılı: {filename} kaydedildi.")

if __name__ == "__main__":
    # 1. Topla
    all_trends = fetch_raw_trends()
    
    # 2. AI ile Süz
    clean_pool = ai_filter_trends(all_trends)
    print(f"AI Onaylı Gündem: {clean_pool}")
    
    # 3. Üret ve Kaydet
    if clean_pool:
        final_output = generate_content(clean_pool)
        save_to_txt(final_output)
        print("Süreç başarıyla tamamlandı.")
