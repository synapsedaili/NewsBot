import os
import requests
import sys
from datetime import datetime
from bs4 import BeautifulSoup

def get_trends():
    # Sadece senin istediğin o dijital kaynaklara bakıyoruz
    print("Trendler kontrol ediliyor...")
    trends = []
    
    # 1. Deneme: Trends24 (X Gündemi) - En hızlı ve canlısı
    try:
        url = "https://trends24.in/turkey/"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        trends = [item.text for item in soup.find('ol').find_all('li')][:10]
    except Exception as e:
        print(f"X trendleri çekilemedi: {e}")

    # 2. Deneme: Eğer X boşsa YouTube Trending'e bak (Alternatif)
    if not trends:
        try:
            # Burası basitleştirilmiş bir örnek, genelde YouTube kazımak zordur
            # ama mantık olarak trend yoksa boş liste dönecek
            pass 
        except:
            pass

    return trends

def generate_content(trends):
    # Trend yoksa sistemi durdur
    if not trends or len(trends) < 3:
        print("Kritik Hata: Yeterli trend verisi bulunamadı. Bugün pas geçiliyor.")
        sys.exit(0) # İşlemi burada bitir, dosya yazma

    prompt = f"""
    Sen @olanlarsakami hesabının ferah ve zeki editörüsün. 
    Şu kelimelerle günün özetini hazırla: {trends}

    [FORMAT]
    - X_THREAD: 5 tweet, emojili, 'Şaka mı bu?' tadında. (Aralarda '---')
    - WEB_ARTICLE: Kısa maddeli, arkadaşça bir 'Günün Analizi'.
    
    NOT: Robotik olma, samimi ol, sadece Türkçe yaz.
    """
    
    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "qwen2.5:1.5b", # Burayı 1.5b yapıyoruz
                "prompt": prompt,
                "stream": False
            }, timeout=150)
        return response.json().get('response', '')
    except:
        return None

def save_to_txt(content):
    if content:
        date_filename = datetime.now().strftime('%d_%m_%Y') + ".txt"
        with open(date_filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Başarılı: {date_filename} oluşturuldu.")

if __name__ == "__main__":
    current_trends = get_trends()
    final_output = generate_content(current_trends)
    save_to_txt(final_output)
