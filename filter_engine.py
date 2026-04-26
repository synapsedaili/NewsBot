import requests

def detect_manipulation(title, summary):
    """Suni gündem ve günah keçisi algılarını tespit eder."""
    keywords = ["oyunlar", "sosyal medya", "müzik", "internet", "video oyun"]
    triggers = ["neden oldu", "katili", "şiddete teşvik", "yüzünden öldü", "bağımlılığı", "akımları"]
    
    title_low = title.lower()
    summary_low = summary.lower()
    
    if any(k in title_low for k in keywords) and any(t in summary_low for t in triggers):
        return True, "Suni Algı / Günah Keçisi Tespiti"
    return False, "Temiz"

def ai_clean_trends(raw_pool):
    print(f"🤖 Llama 3.2 Algı Cerrahı: {len(raw_pool)} içerik taranıyor...")
    processed_data = []
    
    filter_prompt = f"""
    Sen @olanlarsakami Baş Editörüsün. Görevin: Gündemi manipülasyondan arındırmak.

    [ANALİZ KURALLARI]
    1. GERÇEK GÜNDEMİ TUT: Ekonomi, kriz, teknoloji, bilim veya sert toplumsal olayları (RSS, GNews, HN fark etmez) TUT.
    2. ALGIYI SİL: Hedef gösteren, günah keçisi yaratan veya kutuplaştırıcı siyasi polemikleri SİL.
    3. PEMBE HAYALLER YASAK: Gündemi yumuşatma, gerçeği neyse öyle analiz et.

    HABERLER: {raw_pool[:30]}
    
    ÇIKTI FORMATI: Sadece onaylanan maddeleri 'BAŞLIK | ÖZET' formatında yaz, aralarına '###' koy.
    """

    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "llama3.2", 
                "prompt": filter_prompt, 
                "stream": False,
                "options": {"temperature": 0.3} 
            }, timeout=300)
        
        raw_response = response.json().get('response', '').strip()
        results = raw_response.split('###')
        
        for res in results:
            if "|" in res:
                parts = res.split("|", 1)
                title = parts[0].strip()
                summary = parts[1].strip()
                
                is_manipulated, reason = detect_manipulation(title, summary)
                
                processed_data.append({
                    "title": title,
                    "summary": summary,
                    "status": "Blocked" if is_manipulated else "Passed",
                    "reason": reason
                })
        
        return processed_data
    except Exception as e:
        print(f"⚠️ Filtreleme hatası: {e}")
        return []
