import json
from datetime import datetime
from collector import get_all_raw_data
from filter_engine import ai_clean_trends
import requests

def generate_content(trends):
    date_str = datetime.now().strftime('%d.%m.%Y')
    
    # AI'nın kuralları raporlamasını engellemek için doğrudan eylem komutu veriyoruz.
    prompt = f"""
    GÖREVİN: Aşağıdaki haber verilerini kullanarak @olanlarsakami hesabı için bir günlük bülten yazmak. 
    Kuralları teyit etme, sadece bülteni yaz ve bitir.
    
    VERİLER: {trends}
    
    YAZIM KURALLARI:
    1. BAŞLIK: Sadece '{date_str} - Günün Özeti' yaz.
    2. TARZ: Zeki, samimi ve gerçekçi bir dil kullan.
    3. YASAKLI KELİMELER: 'Ferah', 'Huzur', 'Mutluluk', 'Rahatlık' kelimelerini ve türevlerini KESİNLİKLE kullanma.
    4. GERÇEKÇİLİK: Olumlu veya olumsuz ne varsa olduğu gibi aktar, polyannacılık yapma. 
    5. KAPSAM: Sadece teknoloji değil; bilim, sanat, ekonomi ve yaşamdan bahset.
    
    ÇIKTI SADECE HABER METNİ OLMALIDIR. Giriş cümlesi ("İşte bülteniniz", "Anladım") yazma.
    """
    try:
        # Temperature değerini 0.7 yaparak daha doğal, 0.3 yaparak daha kuralcı olmasını sağlayabilirsin.
        r = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "llama3.2", 
                "prompt": prompt, 
                "stream": False,
                "options": {"temperature": 0.6} 
            }, timeout=500)
        
        response_text = r.json().get('response', '').strip()
        
        # Eğer AI hala kuralları sayıklıyorsa, ilk 3 satırı kontrol edip temizleyen basit bir güvenlik önlemi:
        if "Haber Kuralları" in response_text or "Yasaklar" in response_text:
             return "AI kural raporlaması yaptı, tekrar tetikleniyor..."
             
        return response_text
    except: 
        return "İçerik üretilemedi."
if __name__ == "__main__":
    raw = get_all_raw_data()
    analysis = ai_clean_trends(raw)
    passed_trends = [f"{i['title']}: {i['summary']}" for i in analysis if i['status'] == "Passed"]
    
    output = generate_content(passed_trends)
    date_fn = datetime.now().strftime('%d_%m_%Y')
    
    # Dosyaları Kaydet
    with open(f"{date_fn}_ozet.txt", "w", encoding="utf-8") as f: f.write(output)
    
    # Dashboard Verisi
    with open("dashboard.json", "w", encoding="utf-8") as f:
        json.dump({"date": date_fn, "analysis": analysis}, f, ensure_ascii=False, indent=4)
        
    print(f"✅ {date_fn} operasyonu başarıyla tamamlandı. Gürültü elendi, gerçek ortaya çıktı.")
