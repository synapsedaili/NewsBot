import requests
import time
from datetime import datetime
from collector import get_all_raw_data
from filter_engine import ai_clean_trends

def generate_social_content(trends):
    """X/Twitter ve Video Script için kısa, vurucu içerik."""
    prompt = f"""
    Sen @olanlarsakami editörüsün. Tarzın: Samimi kanka dili.
    VERİLER: {trends}
    [GÖREV]
    1. X_THREAD: 5 tweet, aralarında '---' olsun. 'Şaka mı bu?' enerjisiyle başla.
    2. VIDEO_SCRIPT: 60 saniyelik, akıcı seslendirme metni.
    SADECE GERÇEK BİLGİLERİ KULLAN, TÜRKÇE YAZ.
    """
    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={"model": "llama3.2", "prompt": prompt, "stream": False, "options": {"temperature": 0.8}}, timeout=400)
        return response.json().get('response', '').strip()
    except: return "Sosyal medya içeriği üretilemedi."

def generate_web_article(trends):
    """Web sitesi için zengin ve derinlemesine makale."""
    date_str = datetime.now().strftime('%d.%m.%Y')
    prompt = f"""
    Sen @olanlarsakami Baş Editörüsün. Modern ve ferah bir teknoloji/yaşam sitesi için bülten yazıyorsun.
    VERİLER: {trends}
    [GÖREV]
    '{date_str} - Günün Ferah Özeti 🌿' başlığıyla başla. 
    Haberleri birbirine bağlayan, okuyucuya vizyon katan, derinlemesine 4-5 paragraf yaz.
    Maddeler kullanma, akıcı bir makale olsun. SADECE GERÇEK BİLGİLERİ KULLAN.
    """
    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={"model": "llama3.2", "prompt": prompt, "stream": False, "options": {"temperature": 0.6}}, timeout=600)
        return response.json().get('response', '').strip()
    except: return "Web makalesi üretilemedi."

if __name__ == "__main__":
    # 1. Veri Toplama ve Filtreleme
    raw = get_all_raw_data()
    clean = ai_clean_trends(raw)
    
    # 2. Sosyal Medya İçeriği (X ve Video)
    social_text = generate_social_content(clean)
    social_filename = datetime.now().strftime('%d_%m_%Y') + "_social.txt"
    with open(social_filename, "w", encoding="utf-8") as f:
        f.write(social_text)
    
    # 3. Web Makalesi
    web_text = generate_web_article(clean)
    web_filename = datetime.now().strftime('%d_%m_%Y') + "_web.txt"
    with open(web_filename, "w", encoding="utf-8") as f:
        f.write(web_text)
        
    print(f"🚀 İki dosya da başarıyla oluşturuldu: \n1. {social_filename}\n2. {web_filename}")
