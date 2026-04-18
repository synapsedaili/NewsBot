import requests
import time
from datetime import datetime
from collector import get_all_raw_data
from filter_engine import ai_clean_trends

def wait_for_ollama():
    print("⏳ Llama 3.2 hazır mı? Kontrol ediliyor...")
    for _ in range(12):
        try:
            requests.get("http://localhost:11434/api/tags", timeout=5)
            return True
        except: time.sleep(10)
    return False

def generate_final_content(trends):
    date_str = datetime.now().strftime('%d.%m.%Y')
    
    prompt = f"""
    [STRICT RULE: ANSWER ONLY IN TURKISH! ASLA İNGİLİZCE YAZMA!]
    Sen @olanlarsakami editörüsün. Modern, zeki, ferah ve samimi bir tarzın var.
    
    GÜNDEM: {trends}

    [GÖREV]
    Aşağıdaki formatta TEK BİR METİN üret. 
    Dilin 'kanka' samimiyetinde olsun, haber bülteni gibi konuşma. 'Buldu', 'yapıldı' yerine 'keşfetmişler', 'duyurulmuş' gibi doğal ifadeler kullan.

    [FORMAT]
    --- X_THREAD (5 Tweetlik Akış) ---
    - Her tweet arası '---' koy.
    - İlk tweet 'Şaka mı bu?' enerjisiyle başlasın.

    --- WEB_ARTICLE ({date_str} - Günün Ferah Özeti 🌿) ---
    - Gündemdeki olayları maddeler halinde değil, akıcı ve birbirine bağlanan 3-4 paragraf halinde anlat. 
    - İnsanı ferahlatan, vizyon katan bir kapanış yap.
    """
    
    print("✍️ Llama 3.2 Editör koltuğuna oturdu, yazıyor...")
    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 700,
                    "temperature": 0.8 # Daha yaratıcı ve insansı dil
                }
            }, timeout=600)
        return response.json().get('response', 'Hata: Metin boş çıktı.')
    except Exception as e:
        return f"Üretim Hatası: {e}"

if __name__ == "__main__":
    if wait_for_ollama():
        # 1. Havuzu Topla
        raw = get_all_raw_data()
        # 2. AI Süzgecinden Geçir
        clean = ai_clean_trends(raw)
        
        print(f"✅ AI Onaylı Gündem: {clean}")
        
        # 3. Final Metni Üret
        content = generate_final_content(clean)
        
        # 4. Kaydet
        filename = datetime.now().strftime('%d_%m_%Y') + ".txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"🚀 Başarıyla tamamlandı: {filename}")
