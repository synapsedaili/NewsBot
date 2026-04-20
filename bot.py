import requests
import time
from datetime import datetime
from collector import get_all_raw_data
from filter_engine import ai_clean_trends

def generate_social_content(trends):
    """Sosyal medya için sadece Türkçe ve akıcı içerik."""
    prompt = f"""
    [KURAL: SADECE TÜRKÇE YAZ! ASLA İNGİLİZCE KELİME KULLANMA. 'World', 'usage', 'life' gibi kelimeler KESİNLİKLE YASAKTIR.]
    Sen @olanlarsakami editörüsün. Tarzın: Samimi kanka dili.
    VERİLER: {trends}
    
    [GÖREV]
    1. X_THREAD: 5 adet tweet üret. Aralarına '---' koy. (Saniye notu veya teknik bilgi ekleme, sadece tweet metni yaz.)
    2. VIDEO_SCRIPT: 60 saniyelik bir konuşma metni. "Selam kanka, bugün neler olmuş bakalım" diye başla.
    
    Uydurma yapma, sadece elindeki verileri kullan.
    """
    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={"model": "llama3.2", "prompt": prompt, "stream": False, 
                  "options": {"temperature": 0.6, "top_p": 0.9}}, timeout=400)
        return response.json().get('response', '').strip()
    except: return "İçerik üretilemedi."

def generate_web_article(trends):
    """Web için profesyonel ama ferah Türkçe makale."""
    date_str = datetime.now().strftime('%d.%m.%Y')
    prompt = f"""
    [KURAL: SADECE TÜRKÇE YAZ! İngilizce eklerden ve kelimelerden kaçın.]
    Sen @olanlarsakami Baş Editörüsün.
    VERİLER: {trends}
    
    [GÖREV]
    '{date_str} - Günün Ferah Özeti 🌿' başlığıyla başlayan akıcı bir makale yaz. 
    Haberleri birbirine bağla. 'World'sinde', 'Weeks'te' gibi saçma yapılar kurma. Tamamen düzgün, akıcı ve ferah bir Türkçe kullan.
    
    Lütfen her haberi kendi cümlelerinle hikayeleştirerek anlat.
    """
    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={"model": "llama3.2", "prompt": prompt, "stream": False, 
                  "options": {"temperature": 0.4, "top_p": 0.9}}, timeout=600)
        return response.json().get('response', '').strip()
    except: return "Makale üretilemedi."

if __name__ == "__main__":
    # Veri çekme ve temizleme işlemleri aynı kalıyor...
    raw = get_all_raw_data()
    clean = ai_clean_trends(raw)
    
    # Sosyal ve Web dosyalarını üret
    social_text = generate_social_content(clean)
    web_text = generate_web_article(clean)
    
    # Kayıt işlemleri... (social_filename ve web_filename şeklinde kaydet)
