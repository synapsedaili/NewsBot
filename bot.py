#bot.py

import os
import time
import tweepy
import requests
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
from datetime import datetime

def get_google_trends():
    try:
        pytrends = TrendReq(hl='tr-TR', tz=180)
        df = pytrends.trending_searches(pn='turkey')
        return df[0].tolist()[:10]
    except:
        return []

def get_x_trends():
    try:
        url = "https://trends24.in/turkey/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        latest_card = soup.find('div', class_='trend-card')
        return [t.find('a').text for t in latest_card.find_all('li')[:10]]
    except:
        return []

def generate_thread_ollama(google_data, x_data):
    date_str = datetime.now().strftime('%d %B %Y')
    
    prompt = f"""
    Sen '@olanlarsakami' botunun entelektüel editörüsün. Görevin dijital detoks sağlamak.
    
    DATA:
    Google: {google_data}
    X Trends: {x_data}

    RULES:
    - NO POLITICS: Do not include political news or polemics.
    - NO TRASH CONTENT: No magazine, TV series spoilers or reality shows.
    - FOCUS: Tech, science, space, economy, sports and global interest.
    
    FORMAT:
    Tweet 1: "📅 {date_str} | Bugün olanlar şaka mı? \n\nGünün gelişmelerini senin için süzdük. Gürültüyü kenara bıraktık, gerçek gündemle başlıyoruz... 👇"
    Tweet 2-5: Explain selected topics with irony and intelligence. Use '---' as separator.
    Tweet 6: "Gürültüden uzak, temiz bir gündem için takipte kal. İyi geceler. 🌿"
    """
    
    # Ollama local API call
    response = requests.post('http://localhost:11434/api/generate', 
        json={
            "model": "qwen2.5:0.5b", # Using lightweight Qwen for speed in Actions
            "prompt": prompt,
            "stream": False
        })
    
    raw_text = response.json().get('response', '')
    return [t.strip() for t in raw_text.split('---')]

def post_to_x(thread_list):
    client = tweepy.Client(
        consumer_key=os.getenv("X_CONSUMER_KEY"),
        consumer_secret=os.getenv("X_CONSUMER_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET")
    )
    
    last_id = None
    for i, tweet in enumerate(thread_list):
        if tweet and len(tweet) > 5:
            if i == 0:
                response = client.create_tweet(text=tweet)
            else:
                response = client.create_tweet(text=tweet, in_reply_to_tweet_id=last_id)
            last_id = response.data['id']
            time.sleep(3)

if __name__ == "__main__":
    g_trends = get_google_trends()
    x_trends = get_x_trends()
    
    if g_trends or x_trends:
        thread = generate_thread_ollama(g_trends, x_trends)
        post_to_x(thread)