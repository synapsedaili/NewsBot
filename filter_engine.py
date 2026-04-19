import requests

def ai_clean_trends(raw_pool):
    print(f"🤖 Llama 3.2 Gümrükte: {len(raw_pool)} madde inceleniyor...")
    
    # AI'ya daha esnek ama net bir talimat veriyoruz
    filter_prompt = f"""
    Sen @olanlarsakami editörüsün. Aşağıdaki gündem havuzundan 'Dijital Detoks' ruhuna uygun 6-8 madde seç.
    
    [ÖNEMLİ] 
    - Siyaset, bot saldırısı, ağır dram ve küfürlü içerikleri KESİNLİKLE SİL.
    - Ama spor, teknoloji, ilginç yaşam olayları ve bilimsel başlıkları MUTLAKA TUT. 
    - Eğer liste çok kötüyse, içinden en azından 'insanca' olanları seç. 
    
    GÜNDEM: {raw_pool}

    ÇIKTI: Sadece seçtiğin maddeleri virgülle ayırarak yaz. Açıklama yapma.
    """

    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "llama3.2",
                "prompt": filter_prompt,
                "stream": False,
                "options": {"temperature": 0.3} # Biraz daha esnek olması için artırdık
            }, timeout=300)
        
        cleaned = response.json().get('response', '').strip()
        if not cleaned or len(cleaned) < 5:
            # Boş dönmemesi için gerçekçi yedekler
            return ["Yeni Teknoloji Gelişmeleri", "Uzayda Yaşam İzleri", "Yapay Zeka ve Gelecek", "Sağlıklı Yaşam İpuçları"]
        
        return [t.strip() for t in cleaned.split(',') if len(t.strip()) > 2]
    except Exception as e:
        print(f"Filtreleme hatası: {e}")
        return ["Teknoloji", "Bilim", "Gelecek"]
