import requests

def detect_manipulation(title, summary):
    """Suni gündem ve günah keçisi algılarını tespit eder."""
    keywords = ["oyunlar", "sosyal medya", "müzik", "internet", "video oyun"]
    triggers = ["neden oldu", "katili", "şiddete teşvik", "yüzünden öldü", "bağımlılığı"]
    
    # Algı kontrolü
    if any(k in title.lower() for k in keywords) and any(t in summary.lower() for t in triggers):
        return True, "Suni Algı / Günah Keçisi Tespiti"
    return False, "Temiz"

def ai_clean_trends(raw_pool):
    print(f"🤖 Llama 3.2 Radar: {len(raw_pool)} içerik taranıyor...")
    processed_data = []
    
    filter_prompt = f"""
    Sen @olanlarsakami Baş Editörüsün. Aşağıdaki haberleri 'Ferahlık' ve 'Gerçeklik' testinden geçir.
    
    [ANALİZ]
    1. Trajediyi (ölüm, kaza) sadece toplumsal bir ders varsa tut, yoksa SİL.
    2. Bir grubu hedef gösteren (Örn: Oyuncular katildir) algıları SİL.
    
    HABERLER: {raw_pool[:20]}
    
    ÇIKTI: Sadece onaylanan 6 maddeyi 'BAŞLIK | ÖZET' formatında yaz, aralarına '###' koy.
    """

    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={"model": "llama3.2", "prompt": filter_prompt, "stream": False}, timeout=300)
        
        results = response.json().get('response', '').split('###')
        
        for res in results:
            if "|" in res:
                title, summary = res.split("|", 1)
                is_manipulated, reason = detect_manipulation(title, summary)
                processed_data.append({
                    "title": title.strip(),
                    "summary": summary.strip(),
                    "status": "Blocked" if is_manipulated else "Passed",
                    "reason": reason
                })
        return processed_data
    except:
        return []
