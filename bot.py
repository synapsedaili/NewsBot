import json
from datetime import datetime
from collector import get_all_raw_data
from filter_engine import ai_clean_trends
import requests

def generate_content(trends):
    date_str = datetime.now().strftime('%d.%m.%Y')
    
    # Prompt'u AI'nın "halüsinasyon" görmesini engelleyecek şekilde yeniden kurguladık.
    prompt = f"""
    GÖREV: Aşağıdaki haber verilerini analiz et ve @olanlarsakami hesabı için bir bülten oluştur.
    
    VERİLER: {trends}
    
    [KESİN KURALLAR - İHLAL EDİLEMEZ]
    1. DİL: Sadece İstanbul Türkçesi kullan. Aralara İngilizce (presentation, performance vb.) veya başka dillerden kelime ASLA ekleme.
    2. BAŞLIK: Metne sadece '{date_str} - Günün Özeti' başlığıyla başla.
    3. DOĞRULUK: Verilerde olmayan haberleri (Tesla lansmanı, NASA keşfi vb.) kafandan uydurma. Sadece sana verilen listedeki gerçek olayları anlat.
    4. YASAKLI KELİME: 'Ferah', 'Huzur', 'Rahatlık' ve türevlerini kullanmak kesinlikle yasaktır.
    5. GİRİŞ/ÇIKIŞ YASAK: "Merhaba", "İşte haberler", "Lütfen kurallara bakın" gibi cümleler yazma. Doğrudan habere gir ve haberle bitir.
    6. ÜSLUP: Zeki, gerçekçi ve samimi bir 'kanka' dili kullan ama ciddiyeti elden bırakma.
    """
    
    try:
        r = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "llama3.2", 
                "prompt": prompt, 
                "stream": False,
                "options": {
                    "temperature": 0.2, # Halüsinasyonu minimize etmek için düşürdük
                    "top_p": 0.1,
                    "stop": ["Haber Kuralları", "Yasaklar", "Editör Notu"]
                }
            }, timeout=600)
        
        return r.json().get('response', '').strip()
    except: 
        return "Sistem şu an içerik üretemedi, kaynakları kontrol et."

if __name__ == "__main__":
    # Veri Toplama
    raw_data = get_all_raw_data()
    # Algı Cerrahlığı
    analysis = ai_clean_trends(raw_data)
    # Sadece filtreyi geçen gerçek haberler
    passed_trends = [f"{i['title']}: {i['summary']}" for i in analysis if i['status'] == "Passed"]
    
    if not passed_trends:
        print("🚨 Bugün süzgeçten geçebilen temiz bir haber bulunamadı.")
    else:
        # Bülten Üretimi
        final_output = generate_content(passed_trends)
        
        # Dosyayı kaydet
        date_fn = datetime.now().strftime('%d_%m_%Y')
        with open(f"{date_fn}_ozet.txt", "w", encoding="utf-8") as f:
            f.write(final_output)
            
        print(f"✅ Bülten hazır: {date_fn}_ozet.txt")
