import requests

def detect_manipulation(title, summary):
    """Suni gündem ve günah keçisi algılarını tespit eder."""
    keywords = ["oyunlar", "sosyal medya", "müzik", "internet", "video oyun"]
    triggers = ["neden oldu", "katili", "şiddete teşvik", "yüzünden öldü", "bağımlılığı"]
    
    # Algı kontrolü
    if any(k in title.lower() for k in keywords) and any(t in summary.lower() for t in triggers):
        return True, "Suni Algı / Günah Keçisi Tespiti"
    return False, "Temiz"

filter_prompt = f"""
Sen @olanlarsakami Baş Editörüsün. Görevin: Gündemi çiçek-böcek yapmak değil, manipülasyondan arındırmaktır.

[ANALİZ KRİTERLERİ]
1. GERÇEK GÜNDEMİ TUT: Ekonomik krizler, teknolojik savaşlar, bilimsel buluşlar, gerçek toplumsal olaylar... Ne kadar sert olursa olsun, gerçekse TUT.
2. ALGIYI SİL: 'Oyun oynadığı için öldü', 'Şu akımlara kapıldı', 'X partisi şunu dedi' gibi; hedef gösteren, günah keçisi yaratan veya siyasi polemik içeren kısımları SİL.
3. KURGUYU AT: Sosyal medyada tık almak için köpürtülen 'algı yönetimi' haberlerini ele.

[ÖZETLE]
İnsanlara pembe hayaller değil, internetin gürültüsünden arınmış net ve saf gerçeği sun.

HABERLER: {raw_pool}
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
