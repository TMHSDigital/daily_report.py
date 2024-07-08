import requests
import json
import os

def fetch_news(query, category=None):
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    url = 'https://newsapi.org/v2/everything' if query else 'https://newsapi.org/v2/top-headlines'
    params = {
        'q': query,
        'category': category,
        'apiKey': NEWS_API_KEY,
        'pageSize': 5,  # Limit to top 5 articles
    }
    response = requests.get(url, params=params)
    articles = response.json().get('articles', [])
    news = f"{query.title() if query else category.title()} News:\n"
    for article in articles:
        news += f"- {article['title']} ({article['source']['name']}): {article['url']}\n"
    return news

def generate_report():
    ai_news = fetch_news('artificial intelligence')
    stock_news = fetch_news(None, 'business')
    crypto_news = fetch_news('cryptocurrency')
    
    report_content = {
        "ai_news": ai_news,
        "stock_news": stock_news,
        "crypto_news": crypto_news
    }
    
    with open('report.json', 'w') as report_file:
        json.dump(report_content, report_file)

if __name__ == "__main__":
    generate_report()
