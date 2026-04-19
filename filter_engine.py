import requests

def ai_clean_trends(raw_pool):
    print(f"🤖 Llama 3.2: {len(raw_pool)} içerik bloğu inceleniyor...")
    
    filter_prompt = f"""
    Sen @olanlarsakami Baş Editörüsün. Aşağıdaki haber bloklarını incele.
    Siyaset ve dramı ele; bilim, teknoloji ve ilginç yaşam olaylarını seç.
    
    [KRİTİK] Haberlerin içeriğindeki GERÇEK BİLGİLERİ koru. 
    Haber blokları: {raw_pool[:15]}

    ÇIKTI: Seçtiğin 5 bloğu, içeriklerini bozmadan aralarına '|||' koyarak yaz.
    """

    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "llama3.2",
                "prompt": filter_prompt,
                "stream": False,
                "options": {"temperature": 0.2}
            }, timeout=300)
        return response.json().get('response', '').split('|||')
    except:
        return ["Hata: Veri süzülemedi."]
