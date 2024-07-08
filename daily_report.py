import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Replace with your actual API key from NewsAPI
NEWS_API_KEY = '7846c0871ebc45e3b226a9fc6f54eef4'

def fetch_news(query, category=None):
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
    
    report_content = "Daily Report:\n\n"
    report_content += ai_news + "\n"
    report_content += stock_news + "\n"
    report_content += crypto_news + "\n"
    
    # Add the custom note
    report_content += "\nFor more information and custom AI solutions, visit us here: "
    report_content += "https://www.linkedin.com/company/tm-hospitality-strategies/?viewAsMember=true\n"
    
    return report_content

def send_email(report_content):
    # Fetch email credentials from environment variables
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    # Email subject and body
    subject = "Daily Report"
    body = report_content

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the server and send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Using Gmail SMTP server
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    report_content = generate_report()
    send_email(report_content)
