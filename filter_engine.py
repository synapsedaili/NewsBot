import requests

def detect_manipulation(title, summary):
    """Suni gündem ve günah keçisi algılarını tespit eder."""
    # Algı yönetimi için kullanılan anahtar kelimeler
    keywords = ["oyunlar", "sosyal medya", "müzik", "internet", "video oyun"]
    # Algıyı tetikleyen kalıplar
    triggers = ["neden oldu", "katili", "şiddete teşvik", "yüzünden öldü", "bağımlılığı", "akımları"]
    
    title_low = title.lower()
    summary_low = summary.lower()
    
    if any(k in title_low for k in keywords) and any(t in summary_low for t in triggers):
        return True, "Suni Algı / Günah Keçisi Tespiti"
    return False, "Temiz"

def ai_clean_trends(raw_pool):
    print(f"🤖 Llama 3.2 Radar: {len(raw_pool)} içerik taranıyor...")
    processed_data = []
    
    # Prompt'u senin istediğin 'Gerçekçi ve Analitik' felsefeye göre güncelledik
    filter_prompt = f"""
    Sen @olanlarsakami Baş Editörüsün. Görevin: Gündemi çiçek-böcek yapmak değil, manipülasyondan arındırmaktır.

    [ANALİZ KURALLARI]
    1. GERÇEK GÜNDEMİ TUT: Ekonomi, kriz, teknoloji, bilim veya gerçek toplumsal olaylar sert de olsa TUT.
    2. ALGIYI SİL: Hedef gösteren, günah keçisi yaratan (Örn: Oyunlar katildir) veya siyasi polemik içeren kısımları SİL.
    3. KURGUYU AT: Tık almak için köpürtülen 'algı yönetimi' haberlerini ele.

    HABERLER: {raw_pool[:25]}
    
    ÇIKTI FORMATI: Sadece onaylanan maddeleri 'BAŞLIK | ÖZET' formatında yaz, aralarına '###' koy.
    """

    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "llama3.2", 
                "prompt": filter_prompt, 
                "stream": False,
                "options": {"temperature": 0.3} # Daha tutarlı kararlar için düşük sıcaklık
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
