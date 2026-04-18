import requests

def ai_clean_trends(raw_pool):
    print("🤖 Llama 3.2 Gümrükte: Suni gündem ve gürültü ayıklanıyor...")
    
    filter_prompt = f"""
    Sen @olanlarsakami Baş Editörüsün. Aşağıdaki ham gündem listesini 'Dijital Detoks' felsefesiyle süz.
    
    [KURALLAR]
    - Siyaset, tarikat, bot saldırısı (c31k vb.), trajedi, ölüm ve kavga içerenleri SİL.
    - Teknoloji, uzay, bilim, pozitif spor ve vizyon açan haberleri TUT.
    - Eğer madde anlamsız bir isimse (Örn: 'Necmettin Bekçi') onu SİL.

    GÜNDEM HAVUZU: {raw_pool}

    ÇIKTI: Sadece onayladığın en kaliteli 6-8 maddeyi virgülle ayırarak yaz. Başka hiçbir açıklama yapma.
    """

    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "llama3.2",
                "prompt": filter_prompt,
                "stream": False,
                "options": {"temperature": 0.1}
            }, timeout=300)
        
        cleaned = response.json().get('response', '').strip()
        # Eğer AI her şeyi silerse boş dönmemesi için yedek pozitif konular
        if not cleaned or "GENEL" in cleaned:
            return ["Teknoloji", "Gelecek", "Uzay Bilimi", "Pozitif Yaşam"]
        
        return [t.strip() for t in cleaned.split(',') if len(t.strip()) > 2]
    except Exception as e:
        print(f"Filtreleme hatası: {e}")
        return ["Pozitif Gelişmeler", "Bilimsel Haberler", "Teknoloji Dünyası"]
