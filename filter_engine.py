import requests
import json

def ai_clean_trends(raw_pool):
    """Mistral 7B kullanarak anlamsal filtreleme yapar."""
    print("🤖 Mistral Fedai modunda: Suni gündem ayıklanıyor...")
    
    filter_prompt = f"""
    Sen @olanlarsakami Baş Editörüsün. Aşağıdaki karmaşık gündem listesini 'Dijital Detoks' felsefesiyle süz.
    
    [ELEME KURALLARI]
    1. SUNİ GÜNDEM: Bot saldırıları, anlamsız harf dizileri (c31k vb.), tarikat ve troll organizasyonlarını SİL.
    2. TOKSİKLİK: Siyaset, kutuplaşma, kavga, ölüm ve ağır dram içeren her şeyi SİL.
    3. DEĞER: Sadece teknoloji, bilim, spor, uzay ve 'Şaka mı bu?' dedirten pozitif olayları TUT.

    GÜNDEM HAVUZU: {raw_pool}

    [ÇIKTI FORMATI]
    Sadece onayladığın 5-7 maddeyi virgülle ayırarak yaz. Açıklama yapma. 
    Eğer her şey çöp ise sadece 'GENEL_DETOKS' yaz.
    """

    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "mistral",
                "prompt": filter_prompt,
                "stream": False,
                "options": {"temperature": 0.1} # Kararlılık için düşük sıcaklık
            }, timeout=120)
        
        cleaned = response.json().get('response', '').strip()
        if "GENEL_DETOKS" in cleaned:
            return ["Teknoloji", "Uzay", "Bilim", "Dijital Yaşam", "Gelecek"]
        
        return [t.strip() for t in cleaned.split(',') if len(t.strip()) > 2]
    except Exception as e:
        print(f"Filtreleme hatası: {e}")
        return raw_pool[:8] # Hata olursa ham verinin başını ver
