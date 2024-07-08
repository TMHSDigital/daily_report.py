# Daily News Report Automation

This project automates the process of fetching the latest AI news, stock market news, and cryptocurrency news, and sends a daily report via email. The automation is powered by GitHub Actions and uses the NewsAPI to retrieve news articles.

## Features

- Fetches the latest AI news, stock market news, and cryptocurrency news.
- Sends a daily report via email using Gmail SMTP.
- Scheduled to run every day at 9:00 AM UTC.
- Secure storage of sensitive information using GitHub Secrets.

## How It Works

1. **Fetch News**: The script fetches news articles from NewsAPI based on predefined queries.
2. **Generate Report**: The fetched news articles are compiled into a daily report.
3. **Send Email**: The daily report is sent to the specified email address using Gmail SMTP.

## Learn More

[![Visit TM Hospitality Strategies on LinkedIn](https://img.shields.io/badge/Visit%20Us%20on-LinkedIn-blue?logo=linkedin)](https://www.linkedin.com/company/tm-hospitality-strategies/?viewAsMember=true)
[![Powered by NewsAPI](https://img.shields.io/badge/Powered%20by-NewsAPI-red?logo=newsapi)](https://newsapi.org/)

## Setup

### Prerequisites

- Python 3.x
- GitHub account
- NewsAPI account ([Get API Key](https://newsapi.org/))

### Repository Secrets

Add the following secrets to your GitHub repository:

1. `SENDER_EMAIL` - Your email address (e.g., `TMHospitalityStrategies@gmail.com`)
2. `RECEIVER_EMAIL` - Recipient email address (e.g., `TMHospitalityStrategies@gmail.com`)
3. `EMAIL_PASSWORD` - Your email password
4. `NEWS_API_KEY` - Your NewsAPI key

### Steps to Add Secrets

1. Navigate to your repository on GitHub.
2. Click on the "Settings" tab.
3. In the left sidebar, click on "Secrets and variables" and then "Actions".
4. Click on "New repository secret" and add each secret.

### Python Script

Ensure the Python script (`daily_report.py`) uses the environment variables:

```python
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
    
    report_content = "Daily Report:\n\n"
    report_content += ai_news + "\n"
    report_content += stock_news + "\n"
    report_content += crypto_news + "\n"
    
    # Add the custom note
    report_content += "\nFor more information and custom AI solutions, visit us here: "
    report_content += "https://www.linkedin.com/company/tm-hospitality-strategies/?viewAsMember=true\n"
    
    return report_content

def send_email(report_content):
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    password = os.getenv('EMAIL_PASSWORD')

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
```

### GitHub Actions Workflow

Create a GitHub Actions workflow file (`.github/workflows/send_daily_report.yml`):

```yaml
name: Send Daily Report

on:
  workflow_dispatch:
  schedule:
    - cron: '0 9 * * *'  # This will run the workflow at 9:00 AM UTC every day

jobs:
  send_report:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests

      - name: Run Script
        env:
          SENDER_EMAIL: ${{ secrets.SENDER_EMAIL }}
          RECEIVER_EMAIL: ${{ secrets.RECEIVER_EMAIL }}
          EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
          NEWS_API_KEY: ${{ secrets.NEWS_API_KEY }}
        run: python daily_report.py
```

## Running the Workflow

You can manually trigger the workflow from the Actions tab in your GitHub repository or wait for the scheduled time (9:00 AM UTC) for it to run automatically.

## License

This project is licensed under the MIT License.

---

For more information and custom AI solutions, visit us on [LinkedIn](https://www.linkedin.com/company/tm-hospitality-strategies/?viewAsMember=true).

[![Visit TM Hospitality Strategies on LinkedIn](https://img.shields.io/badge/Visit%20Us%20on-LinkedIn-blue?logo=linkedin)](https://www.linkedin.com/company/tm-hospitality-strategies/?viewAsMember=true)
[![Powered by NewsAPI](https://img.shields.io/badge/Powered%20by-NewsAPI-red?logo=newsapi)](https://newsapi.org/)
```
