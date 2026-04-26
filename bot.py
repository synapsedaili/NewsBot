import requests
import json
from datetime import datetime
from collector import get_all_raw_data
from filter_engine import ai_clean_trends

def generate_content(trends, mode="social"):
    """Moduna göre (social/web) içerik üretir."""
    persona = "enerjik kanka" if mode == "social" else "bilge teknoloji filozofu"
    temp = 0.85 if mode == "social" else 0.4
    date_str = datetime.now().strftime('%d.%m.%Y')
    
    # "Ferah" kelimesi burada kesin olarak yasaklanıyor.
    prompt = f"""
    Sen @olanlarsakami hesabının {persona} editörüsün. 
    Veriler: {trends}
    
    [GÖREV] 
    Sadece Türkçe kullanarak, vizyoner bir içerik üret. 
    
    [KESİN YASAK] 
    'Ferah', 'Ferahlık', 'Günün ferah özeti' gibi kelimeleri ASLA kullanma. 
    Başlıkta sadece '{date_str} - Günün Özeti' veya '{date_str} - Neler Oldu?' gibi sade bir yapı kullan.
    
    [TARZ] 
    Duyguyu kelimelerle değil, seçtiğin haberlerin kalitesiyle ve anlatımındaki sadelikle hissettir. 
    Llama dilindeki 'world', 'usage' gibi saçma İngilizce ekleri temizle, öz Türkçe ve akıcı konuş.
    """
    
    try:
        r = requests.post('http://localhost:11434/api/generate', 
            json={"model": "llama3.2", "prompt": prompt, "stream": False, "options": {"temperature": temp}}, timeout=500)
        return r.json().get('response', '').strip()
    except: return "İçerik üretilemedi."

if __name__ == "__main__":
    # 1. Veri Topla
    raw = get_all_raw_data()
    # 2. Radar Analizi (Yeni Yapı)
    analysis_results = ai_clean_trends(raw)
    
    # Onaylananları filtrele
    passed_trends = [f"{item['title']}: {item['summary']}" for item in analysis_results if item['status'] == "Passed"]
    
    # 3. İçerikleri Üret
    social_text = generate_content(passed_trends, "social")
    web_text = generate_content(passed_trends, "web")
    
    # 4. Dosyaları ve Dashboard Verisini Kaydet
    date_str = datetime.now().strftime('%d_%m_%Y')
    
    # Klasik dosyalar
    with open(f"{date_str}_social.txt", "w", encoding="utf-8") as f: f.write(social_text)
    with open(f"{date_str}_web.txt", "w", encoding="utf-8") as f: f.write(web_text)
    
    # Dashboard Verisi (JSON)
    dashboard_entry = {
        "date": date_str,
        "analysis": analysis_results,
        "social_preview": social_text[:200] + "..."
    }
    
    # dashboard.json dosyasını güncelle veya oluştur
    try:
        with open("dashboard.json", "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append(dashboard_entry)
            f.seek(0)
            json.dump(data[-10:], f, ensure_ascii=False, indent=4) # Son 10 günü tut
    except:
        with open("dashboard.json", "w", encoding="utf-8") as f:
            json.dump([dashboard_entry], f, ensure_ascii=False, indent=4)

    print("🚀 Radar taraması bitti, içerikler üretildi ve Dashboard güncellendi!")
