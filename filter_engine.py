import requests

def ai_clean_trends(raw_pool):
    print("🤖 Mistral Fedai: Gündem süzgeci başlıyor...")
    
    filter_prompt = f"""
    Sen @olanlarsakami Baş Editörüsün. Aşağıdaki gündem listesini 'Dijital Detoks' felsefesiyle süz.
    
    [ELEME] Bot saldırıları, siyaset, dram, ölüm ve tarikat taglerini SİL.
    [TUT] Teknoloji, uzay, bilim, pozitif spor ve 'Şaka mı bu?' olaylarını TUT.

    GÜNDEM HAVUZU: {raw_pool}

    ÇIKTI: Sadece onaylanan 5-7 maddeyi virgülle ayırarak yaz. Başka hiçbir şey yazma.
    """

    try:
        # Filtreleme için de timeout'u garantiye alalım
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "mistral",
                "prompt": filter_prompt,
                "stream": False,
                "options": {"temperature": 0.1}
            }, timeout=300)
        
        cleaned = response.json().get('response', '').strip()
        if not cleaned or "GENEL_DETOKS" in cleaned:
            return ["Teknoloji", "Gelecek", "Uzay", "Bilim", "Dijital Sanat"]
        
        return [t.strip() for t in cleaned.split(',') if len(t.strip()) > 2]
    except Exception as e:
        print(f"Filtreleme hatası: {e}")
        return ["Pozitif Yaşam", "Gelecek Teknolojileri", "Uzay Keşfi"]
