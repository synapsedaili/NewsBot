import requests
import json
from datetime import datetime
from collector import get_all_raw_data
from filter_engine import ai_clean_trends

def generate_content(trends, mode="social"):
    persona = "gerçekçi ve analiz yapan bir dost" if mode == "social" else "stratejik bir gözlemci"
    temp = 0.5 # Daha ciddi ve verilere sadık kalması için düşürdük
    
    prompt = f"""
    Sen @olanlarsakami editörüsün. Elindeki liste internetin gürültüsünden arındırılmış gerçek gündemdir: {trends}
    
    [GÖREV] 
    Haberleri basitleştirme veya 'iyiye yorma'. Ne olduysa onu net, samimi ve zeki bir dille anlat. 
    
    [YASAKLAR]
    - 'Çiçek, böcek, pembe hayaller' gibi aşırı pozitif ve boş ifadeler kullanma.
    - Siyasetin kutuplaştırıcı diline girme.
    - 'Ferah' kelimesi yasak.
    - 'Usage', 'World' gibi plaza Türkçesi yasak.
    
    [BAŞLIK] 
    Sadece '{datetime.now().strftime('%d.%m.%Y')} - Günün Özeti'
    """

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
