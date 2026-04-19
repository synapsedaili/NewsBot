import requests
import time
from datetime import datetime
from collector import get_all_raw_data
from filter_engine import ai_clean_trends

def wait_for_ollama():
    print("⏳ Llama 3.2 servisi kontrol ediliyor...")
    for _ in range(15): # Bekleme süresini biraz daha uzattık
        try:
            requests.get("http://localhost:11434/api/tags", timeout=5)
            return True
        except: time.sleep(10)
    return False

def generate_final_content(trends):
    date_str = datetime.now().strftime('%d.%m.%Y')
    
    # Prompt'u daha 'yazmaya zorlayıcı' hale getirdik
    prompt = f"""
    Sen @olanlarsakami editörüsün. Elinde şu tertemiz gündem maddeleri var: {trends}
    
    [GÖREV]
    Bu maddeleri kullanarak samimi, kanka tarzında bir günlük bülten yaz.
    
    [FORMAT]
    --- X_THREAD ---
    (5 tweet, aralarda --- olsun)
    
    --- WEB_ARTICLE ({date_str}) ---
    (3-4 paragraf akıcı metin)

    [KRİTİK] 
    Sadece TÜRKÇE yaz. Boş çıktı üretme. Eğer konu bulamazsan genel bir dijital yaşam tavsiyesi ver.
    """
    
    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 1000, # Çıktı kapasitesini artırdık
                    "temperature": 0.7
                }
            }, timeout=600)
        
        res_data = response.json()
        output = res_data.get('response', '').strip()
        
        if not output:
            return "Hata: AI metin üretmeyi reddetti veya boş bıraktı."
        return output
    except Exception as e:
        return f"Üretim Hatası: {e}"

if __name__ == "__main__":
    if wait_for_ollama():
        raw = get_all_raw_data()
        clean = ai_clean_trends(raw)
        
        print(f"✅ AI Onaylı Gündem: {clean}")
        
        # Isınma molası: AI'nın kendine gelmesi için 5 saniye
        time.sleep(5) 
        
        content = generate_final_content(clean)
        
        # Boş metin kontrolü
        if len(content) < 50:
            print("⚠️ Metin çok kısa veya boş, tekrar deneniyor...")
            content = generate_final_content(clean)

        filename = datetime.now().strftime('%d_%m_%Y') + ".txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"🚀 Dosya kaydedildi: {filename}")
