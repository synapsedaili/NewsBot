import requests
import time
import os
from datetime import datetime
from collector import get_all_raw_data
from filter_engine import ai_clean_trends

def wait_for_ollama():
    print("⏳ Llama 3.2 servisi kontrol ediliyor...")
    for _ in range(15):
        try:
            requests.get("http://localhost:11434/api/tags", timeout=5)
            print("✅ Ollama Hazır!")
            return True
        except:
            time.sleep(10)
    return False

def generate_social_content(trends):
    print("✍️ Sosyal medya içeriği yazılıyor...")
    prompt = f"""
    [KURAL: SADECE TÜRKÇE YAZ! 'World', 'usage', 'life' gibi kelimeler KESİNLİKLE YASAKTIR.]
    Sen @olanlarsakami editörüsün. Tarzın: Samimi kanka dili.
    VERİLER: {trends}
    
    [GÖREV]
    1. X_THREAD: 5 adet tweet üret. Aralarına '---' koy. 
    2. VIDEO_SCRIPT: 60 saniyelik bir konuşma metni. "Selam kanka, bugün neler olmuş bakalım" diye başla.
    
    Teknik not yazma, sadece doğrudan metni yaz.
    """
    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={"model": "llama3.2", "prompt": prompt, "stream": False, 
                  "options": {"temperature": 0.6, "top_p": 0.9}}, timeout=400)
        return response.json().get('response', '').strip()
    except Exception as e:
        return f"Sosyal Medya Hatası: {e}"

def generate_web_article(trends):
    print("✍️ Web makalesi yazılıyor...")
    date_str = datetime.now().strftime('%d.%m.%Y')
    prompt = f"""
    [KURAL: SADECE TÜRKÇE YAZ!]
    Sen @olanlarsakami Baş Editörüsün.
    VERİLER: {trends}
    
    [GÖREV]
    '{date_str} - Günün Ferah Özeti 🌿' başlığıyla başlayan akıcı bir makale yaz. 
    Haberleri birbirine bağla. Plaza Türkçesi kullanma, düzgün ve ferah bir Türkçe kullan.
    """
    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={"model": "llama3.2", "prompt": prompt, "stream": False, 
                  "options": {"temperature": 0.4, "top_p": 0.9}}, timeout=600)
        return response.json().get('response', '').strip()
    except Exception as e:
        return f"Web Makale Hatası: {e}"

if __name__ == "__main__":
    if wait_for_ollama():
        # 1. Veri Toplama ve Filtreleme
        raw = get_all_raw_data()
        clean = ai_clean_trends(raw)
        
        print(f"✅ AI Onaylı Gündem Alındı. Dosyalar yazılıyor...")

        # 2. İçerikleri Üret
        social_text = generate_social_content(clean)
        web_text = generate_web_article(clean)
        
        # 3. Dosyaları Kaydet (BURASI KRİTİK!)
        date_prefix = datetime.now().strftime('%d_%m_%Y')
        
        social_filename = f"{date_prefix}_social.txt"
        with open(social_filename, "w", encoding="utf-8") as f:
            f.write(social_text)
            
        web_filename = f"{date_prefix}_web.txt"
        with open(web_filename, "w", encoding="utf-8") as f:
            f.write(web_text)
            
        print(f"🚀 İşlem Tamamlandı!")
        print(f"1. {social_filename} oluşturuldu.")
        print(f"2. {web_filename} oluşturuldu.")
    else:
        print("❌ Ollama başlatılamadı, işlem iptal.")
