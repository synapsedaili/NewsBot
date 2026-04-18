import requests
from datetime import datetime
from collector import get_all_raw_data
from filter_engine import ai_clean_trends

def generate_final_content(trends):
    """Mistral 7B ile Türkçe ferah içerik üretir."""
    date_str = datetime.now().strftime('%d.%m.%Y')
    
    prompt = f"""
    [STRICT RULE: ANSWER ONLY IN TURKISH!]
    Sen @olanlarsakami editörüsün. Tarzın: Modern, zeki ve ferah.
    
    Gündem: {trends}

    [GÖREV]
    1. X_THREAD: 5 tweet (--- ile ayır). 'Şaka mı bu?' enerjisinde olsun.
    2. WEB_ARTICLE: '{date_str} - Günün Ferah Özeti 🌿' başlığıyla samimi bir özet.

    Karakter hatalarını düzelt. Siyaseti ve dramı asla dahil etme. SADECE TÜRKÇE YAZ.
    """
    
    print("✍️ Mistral Editör modunda: Metin yazılıyor...")
    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.7, "num_predict": 1000}
            }, timeout=300)
        return response.json().get('response', 'Hata: İçerik boş.')
    except Exception as e:
        return f"Üretim Hatası: {e}"

if __name__ == "__main__":
    raw_data = get_all_raw_data()
    clean_data = ai_clean_trends(raw_data)
    
    if clean_data:
        content = generate_final_content(clean_data)
        filename = datetime.now().strftime('%d_%m_%Y') + ".txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"🚀 Başarılı: {filename} hazır!")
