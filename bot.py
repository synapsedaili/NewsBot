import requests
from datetime import datetime
from collector import get_all_raw_data
from filter_engine import ai_clean_trends

def generate_final_content(trends):
    date_str = datetime.now().strftime('%d.%m.%Y')
    
    prompt = f"""
    Sen @olanlarsakami editörüsün. Elinde şu GERÇEK içerikler var: {trends}
    
    Bu bilgilere sadık kalarak (uydurma yapmadan) şu bölümleri oluştur:

    --- X_THREAD (Twitter) ---
    - 5 Tweet. Samimi, ironik ve ferah. Aralara '---' koy.
    
    --- VIDEO_SCRIPT (Kısa Video İçin) ---
    - Maksimum 60 saniyelik, heyecanlı ve akıcı bir anlatım metni. 
    - Giriş: "Bugün internette neler mi oldu? Hemen anlatıyorum!"
    
    --- WEB_ARTICLE ({date_str}) ---
    - Başlık ve 3 derinlemesine paragraf. Detayları içerikten al, uydurma.

    DİL: TÜRKÇE. Tarz: Modern ve zeki.
    """
    
    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False,
                "options": {"num_predict": 1200, "temperature": 0.7}
            }, timeout=600)
        return response.json().get('response', '').strip()
    except Exception as e:
        return f"Hata: {e}"

if __name__ == "__main__":
    # 1. İçerikli veriyi çek
    raw = get_all_raw_data()
    # 2. AI süzgecinden geçir
    clean = ai_clean_trends(raw)
    # 3. Üçlü formatta metni yaz
    final_output = generate_final_content(clean)

    filename = datetime.now().strftime('%d_%m_%Y') + ".txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_output)
    print(f"🚀 Video, X ve Web içerikleri hazır: {filename}")
