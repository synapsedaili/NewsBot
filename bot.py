import json
from datetime import datetime
from collector import get_all_raw_data
from filter_engine import ai_clean_trends
import requests

def generate_content(trends):
    date_str = datetime.now().strftime('%d.%m.%Y')
    prompt = f"""
    Sen @olanlarsakami editörüsün. Elindeki veri internetin gürültüsünden arınmış saf gerçeği temsil ediyor: {trends}
    
    [GÖREV]
    Haberleri net, zeki ve samimi bir dille anlat. 
    BAŞLIK FORMATI: '{date_str} - Günün Özeti'
    
    [YASAKLAR]
    - 'Ferah' kelimesi ve türevleri KESİNLİKLE YASAK.
    - Pembe tablo çizmek, çiçek-böcek edebiyatı yasAK.
    - Sadece teknolojiye odaklanmak yasak; hayatın her alanından bahset.
    """
    try:
        r = requests.post('http://localhost:11434/api/generate', 
            json={"model": "llama3.2", "prompt": prompt, "stream": False}, timeout=500)
        return r.json().get('response', '').strip()
    except: return "İçerik üretilemedi."

if __name__ == "__main__":
    raw = get_all_raw_data()
    analysis = ai_clean_trends(raw)
    passed_trends = [f"{i['title']}: {i['summary']}" for i in analysis if i['status'] == "Passed"]
    
    output = generate_content(passed_trends)
    date_fn = datetime.now().strftime('%d_%m_%Y')
    
    # Dosyaları Kaydet
    with open(f"{date_fn}_ozet.txt", "w", encoding="utf-8") as f: f.write(output)
    
    # Dashboard Verisi
    with open("dashboard.json", "w", encoding="utf-8") as f:
        json.dump({"date": date_fn, "analysis": analysis}, f, ensure_ascii=False, indent=4)
        
    print(f"✅ {date_fn} operasyonu başarıyla tamamlandı. Gürültü elendi, gerçek ortaya çıktı.")
