import requests
import time
from datetime import datetime
from collector import get_all_raw_data
from filter_engine import ai_clean_trends

def generate_final_content(trends):
    date_str = datetime.now().strftime('%d.%m.%Y')
    
    # AI'ya bir karakter (Persona) veriyoruz, reddetmesi zorlaşır
    prompt = f"""
    ### SYSTEM ###
    Sen eğlenceli, zeki ve asla pes etmeyen bir sosyal medya içerik üreticisisin. 
    İşin, sıkıcı gündemi ferahlatmak. 
    
    ### GÜNDEM ###
    {trends}

    ### GÖREV ###
    1. X_THREAD (5 Tweet, --- ayraçlı)
    2. WEB_ARTICLE (3-4 akıcı paragraf)
    
    ### KURALLAR ###
    - DİL: TÜRKÇE.
    - SAMİMİYET: Maksimum (Kanka dili).
    - Reddetmek yok, eldeki veriyi en iyi şekilde işle.
    """
    
    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 1000,
                    "temperature": 0.8
                }
            }, timeout=600)
        
        output = response.json().get('response', '').strip()
        return output if len(output) > 50 else None
    except: return None

if __name__ == "__main__":
    # Ollama bekleme, Veri toplama, Filtreleme ve Yazma
    raw = get_all_raw_data()
    clean = ai_clean_trends(raw)
    print(f"✅ Hazırlanan Gündem: {clean}")
    
    content = generate_final_content(clean)
    
    # Eğer AI hala inat ediyorsa (Empty output), bir acil durum metni üret
    if not content:
        print("⚠️ AI sustu, acil durum metni devreye giriyor...")
        # Basit bir yedek mekanizma veya manuel müdahale için log bas
        content = "Günün bülteni hazırlanırken bir teknik aksaklık oldu ama ferah kalmaya devam ediyoruz! 🌿"

    filename = datetime.now().strftime('%d_%m_%Y') + ".txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"🚀 Süreç bitti: {filename}")
