import os
import requests
from datetime import datetime

def get_trends():
    # Trends fetching logic remains here (Pytrends/Trends24)
    # Simplifying for the draft
    return ["Tech Trends", "Space Exploration", "AI Innovation"]

def generate_content(trends):
    date_str = datetime.now().strftime('%d.%m.%Y')
    
    # Prompting Qwen to generate both X Thread and Web Article
    prompt = f"""
    Role: Intellectual editor for '@olanlarsakami'.
    Task: Create content for {date_str} based on: {trends}.
    
    Format:
    [X_THREAD]
    (Write 5-6 tweets in Turkish, use '---' between them)
    
    [WEB_ARTICLE]
    (Write a detailed, 300-word intellectual blog post in Turkish)
    """
    
    response = requests.post('http://localhost:11434/api/generate', 
        json={
            "model": "qwen2.5:0.5b",
            "prompt": prompt,
            "stream": False
        })
    return response.json().get('response', '')

def save_to_txt(content):
    date_filename = datetime.now().strftime('%d_%m_%Y') + ".txt"
    with open(date_filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Content saved to {date_filename}")

if __name__ == "__main__":
    trends = get_trends()
    full_content = generate_content(trends)
    save_to_txt(full_content)
