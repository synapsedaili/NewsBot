import requests

def ai_clean_trends(raw_pool):
    print(f"🤖 Llama 3.2: {len(raw_pool)} madde süzgeçten geçiyor...")
    
    # AI'ya 'reddetme' şansı bırakmayan yeni prompt
    filter_prompt = f"""
    Sen @olanlarsakami editörüsün. Aşağıdaki listeden en 'ilginç' 10 maddeyi seç.
    
    HAVUZ: {raw_pool[:100]} 

    [ÖNCELİK]
    Teknoloji, bilim, uzay, oyun, spor başarıları ve garip dünya haberleri.
    
    [YASAK]
    Sadece aşırı küfürlü veya yasadışı olanları ele. Siyasi tartışmaları görmezden gel.
    
    ÇIKTI: Sadece maddeleri virgülle yaz.
    """

    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "llama3.2",
                "prompt": filter_prompt,
                "stream": False,
                "options": {"temperature": 0.5} 
            }, timeout=300)
        
        cleaned = response.json().get('response', '').strip()
        if len(cleaned) < 10:
            return ["Yapay Zeka", "Uzay Keşfi", "Gelecek Teknolojileri", "Dijital Sanat"]
        return [t.strip() for t in cleaned.split(',') if len(t.strip()) > 2]
    except:
        return ["Teknoloji", "Bilim", "Gelecek"]
