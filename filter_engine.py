import requests

def detect_manipulation(title, summary):
    # Anahtar kelimeleri biraz daha spesifikleştiriyoruz ki masum haberler yanmasın
    keywords = ["oyunlar", "video oyun", "sosyal medya akımı"]
    triggers = ["katili", "yüzünden öldü", "şiddete teşvik", "bağımlılığı"]
    
    content = (title + " " + summary).lower()
    # Sadece hem keyword hem trigger varsa blokla
    if any(k in content for k in keywords) and any(t in content for t in triggers):
        return True, "Suni Algı Tespiti"
    return False, "Temiz"

def ai_clean_trends(raw_pool):
    print(f"🤖 Algı Cerrahı {len(raw_pool)} içeriği inceliyor...")
    processed_data = []
    
    # AI'ya 'gri alanları' kabul etmesini söylüyoruz
    filter_prompt = f"""
    Sen @olanlarsakami Baş Editörüsün. Görevin internetin gürültüsünü temizlemek ama GERÇEK GÜNDEMİ kaçırmamak.

    [FİLTRELEME REHBERİ]
    1. TUT: Ekonomi haberleri, bilimsel buluşlar, teknolojik duyurular, resmi devlet açıklamaları, sanat ve spor haberleri. (Sert de olsa gerçekse tut.)
    2. SİL: "X oyunu intihara sürükledi", "Şu şarkı gençliği bozuyor" gibi temelsiz suçlamaları ve sadece polemik amaçlı boş siyasi tartışmaları sil.
    3. KRİTER: Haber bir 'bilgi' mi veriyor yoksa bir 'algı' mı yaratıyor? Bilgi veriyorsa TUT.

    VERİLER: {raw_pool[:40]}
    
    ÇIKTI FORMATI: Sadece onayladığın haberleri 'BAŞLIK | ÖZET' olarak yaz ve aralarına '###' koy. 
    Eğer hepsi kötüyse bile, içlerinden en 'bilgi odaklı' olan 5 tanesini seçmek zorundasın.
    """

    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "llama3.2", 
                "prompt": filter_prompt, 
                "stream": False,
                "options": {"temperature": 0.4} # Biraz daha esneklik için artırdık
            }, timeout=300)
        
        raw_res = response.json().get('response', '').strip()
        results = raw_res.split('###')
        
        for res in results:
            if "|" in res:
                title, summary = res.split("|", 1)
                is_manipulated, reason = detect_manipulation(title, summary)
                # Manuel fonksiyon engellemedikçe AI'nın geçtiği haberi kabul et
                processed_data.append({
                    "title": title.strip(),
                    "summary": summary.strip(),
                    "status": "Blocked" if is_manipulated else "Passed",
                    "reason": reason
                })
        return processed_data
    except:
        return []
