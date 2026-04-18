import requests
import time
from datetime import datetime
from collector import get_all_raw_data
from filter_engine import ai_clean_trends

def wait_for_ollama():
    """Ollama servisinin hazır olmasını bekler."""
    print("⏳ Ollama servis kontrolü...")
    for i in range(10):
        try:
            requests.get("http://localhost:11434/api/tags", timeout=5)
            print("✅ Ollama hazır!")
            return True
        except:
            time.sleep(10)
    return False

def generate_final_content(trends):
    date_str = datetime.now().strftime('%d.%m.%Y')
    prompt = f"""
    [STRICT RULE: ANSWER ONLY IN TURKISH!]
    Sen @olanlarsakami editörüsün. Modern ve ferah bir dille yaz.
    Gündem: {trends}
    [GÖREV] 
    1. X_THREAD: 5 tweet (--- ayıracıyla).
    2. WEB_ARTICLE: '{date_str} - Günün Ferah Özeti 🌿' başlığıyla samimi bir bülten.
    Dramdan ve siyasetten uzak dur.
    """
    
    print("✍️ Mistral içerik üretiyor (Bu işlem 10 dakikaya kadar sürebilir)...")
    try:
        # TIMEOUT BURADA 600 SANİYEYE ÇIKARILDI
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False,
                "options": {"num_predict": 800, "temperature": 0.7}
            }, timeout=900) 
        return response.json().get('response', 'İçerik boş.')
    except Exception as e:
        return f"Üretim Hatası (Timeout): {e}"

if __name__ == "__main__":
    if wait_for_ollama():
        raw_data = get_all_raw_data()
        clean_data = ai_clean_trends(raw_data)
        
        content = generate_final_content(clean_data)
        filename = datetime.now().strftime('%d_%m_%Y') + ".txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"🚀 İşlem tamam: {filename}")
