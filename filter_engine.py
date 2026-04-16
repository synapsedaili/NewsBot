# filter_engine.py

# Kara Liste: Girmeyecek kelimeler/gruplar
BLACKLIST = [
    "furkan", "hoca", "tarikat", "şeriat", "konferans", "tebliğ", # Tarikatçılar
    "erdoğan", "akp", "chp", "mhp", "belediye", "seçim", "istifa", # Siyaset
    "katliam", "ölüm", "kaza", "cinayet", "tutuklansın", "taciz", # Ağır Dram
    "hapis", "adliye", "vaka", "operasyon", "şehit" # Askeri/Adli
]

# Beyaz Liste: Gördüğünde "Bu kesin kalsın" dediğimiz konular
WHITELIST = [
    "teknoloji", "yapay zeka", "uzay", "bilim", "fenerbahçe", "galatasaray", 
    "beşiktaş", "voleybol", "melekler", "nba", "f1", "yks", "nasa", "apple", "nvidia"
]

def clean_trends(raw_list):
    """
    Gelen devasa listeyi süzgeçten geçirir.
    """
    cleaned = []
    for trend in raw_list:
        t_lower = trend.lower()
        
        # 1. Kural: Kara listedeyse anında ele
        if any(bad in t_lower for bad in BLACKLIST):
            continue
            
        # 2. Kural: Beyaz listedeyse öncelik ver (başa ekle)
        if any(good in t_lower for good in WHITELIST):
            cleaned.insert(0, trend)
            continue
            
        # 3. Kural: Çok kısa veya sadece sayıdan oluşanları ele
        if len(trend) < 3 or trend.isdigit():
            continue
            
        cleaned.append(trend)
        
    # Tekrar edenleri temizle ve ilk 15 en kaliteli veriyi döndür
    return list(dict.fromkeys(cleaned))[:15]
