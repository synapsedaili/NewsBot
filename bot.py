import os
import requests
from datetime import datetime
from pytrends.request import TrendReq

def get_filtered_trends():
    try:
        pytrends = TrendReq(hl='tr-TR', tz=180)
        # Türkiye gündemini çek
        df = pytrends.trending_searches(pn='turkey')
        all_trends = df[0].tolist()
        
        # İlk 10 trendi al (Siyaset dışı kalmaya çalışarak)
        return all_trends[:10]
    except Exception as e:
        print(f"Trend çekme hatası: {e}")
        return ["Teknoloji", "Bilim", "Uzay", "Spor", "Yaşam"]

def generate_content(trends):
    date_str = datetime.now().strftime('%d.%m.%Y')
    
    # Senin istediğin "Ferah ve Canlı" dil talimatı
    prompt = f"""
    [ROLE]
    Sen '@olanlarsakami' editörüsün. Modern, ferah ve hafif ironik bir dilin var.
    [DATA]
    Günün kelimeleri: {trends}
    [TASK]
    1. X_THREAD: 5 tweetlik, emojili, 'Şaka mı bu?' enerjisinde bir akış yaz. (Aralara '---' koy)
    2. WEB_ARTICLE: Günün özeti başlığıyla, boğucu olmayan, kısa maddeli bir yazı yaz.
    DİL: Türkçe. Siyasetten uzak dur, spor ve teknolojiye odaklan.
    """
    
    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "qwen2.5:0.5b",
                "prompt": prompt,
                "stream": False
            }, timeout=120)
        return response.json().get('response', 'AI yanıt üretemedi.')
    except:
        return "Bağlantı hatası: Qwen yanıt vermedi."

def save_to_txt(content):
    date_filename = datetime.now().strftime('%d_%m_%Y') + ".txt"
    with open(date_filename, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    trends = get_filtered_trends()
    content = generate_content(trends)
    save_to_txt(content)
