import requests

def detect_manipulation(title, summary):
    """Suni gündem ve günah keçisi algılarını tespit eder."""
    # Trendlerde köpürtülen anahtar kelimeler
    keywords = ["oyunlar", "sosyal medya", "müzik", "internet", "video oyun", "yasaklansın"]
    triggers = ["neden oldu", "katili", "şiddete teşvik", "yüzünden öldü", "bağımlılığı", "akımları"]
    
    content = (title + " " + summary).lower()
    if any(k in content for k in keywords) and any(t in content for t in triggers):
        return True, "Suni Algı / Günah Keçisi Operasyonu"
    return False, "Temiz"

def ai_clean_trends(raw_pool):
    print(f"🤖 Algı Cerrahı {len(raw_pool)} içeriği inceliyor...")
    processed_data = []
    
    filter_prompt = f"""
    Sen @olanlarsakami Baş Editörüsün. Görevin: Gündemi manipülasyondan ve suni 'linç' kültüründen arındırmak.
    
    [ANALİZ KURALLARI]
    1. GERÇEK GÜNDEM: Ekonomi, kriz, bilim, teknoloji gibi somut olayları ne kadar sert olursa olsun TUT.
    2. SUNİ ALGI: 'X oyunu yüzünden öldü', 'Şu grup yasaklansın' gibi hedef gösteren algıları DERHAL SİL.
    3. GERÇEKÇİ OL: Pembe hayaller kurma, ferahlığı 'gerçeği yalansız sunarak' sağla.
    
    HABERLER: {raw_pool[:30]}
    
    ÇIKTI: 'BAŞLIK | ÖZET' şeklinde, her haber arasına '###' koy.
    """

    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={"model": "llama3.2", "prompt": filter_prompt, "stream": False, "options": {"temperature": 0.3}}, 
            timeout=300)
        
        results = response.json().get('response', '').split('###')
        for res in results:
            if "|" in res:
                title, summary = res.split("|", 1)
                is_manipulated, reason = detect_manipulation(title, summary)
                processed_data.append({
                    "title": title.strip(), "summary": summary.strip(),
                    "status": "Blocked" if is_manipulated else "Passed", "reason": reason
                })
        return processed_data
    except: return []
