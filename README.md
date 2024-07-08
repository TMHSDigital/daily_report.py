# Daily News Report Automation

This project automates the process of fetching the latest AI news, stock market news, and cryptocurrency news, and sends a daily report via email or displays it on a web interface. The automation is powered by GitHub Actions and uses the NewsAPI to retrieve news articles.

## Features

- Fetches the latest AI news, stock market news, and cryptocurrency news.
- Sends a daily report via email using Gmail SMTP.
- Generates a daily report as a JSON file for a web interface.
- Scheduled to run every day at 9:00 AM UTC for the email version.
- Secure storage of sensitive information using GitHub Secrets.

## Badges

[![Visit TM Hospitality Strategies on LinkedIn](https://img.shields.io/badge/Visit%20Us%20on-LinkedIn-blue?logo=linkedin)](https://www.linkedin.com/company/tm-hospitality-strategies/?viewAsMember=true)
[![Powered by NewsAPI](https://img.shields.io/badge/Powered%20by-NewsAPI-red?logo=newsapi)](https://newsapi.org/)

## Repository Structure

```
/daily_report
  /email_version
    - daily_report_email.py
  /web_version
    - daily_report_web.py
    - index.html
    - styles.css
    - script.js
/.github
  /workflows
    - send_daily_report.yml
```

## Email Version

### Setup

#### Prerequisites

- Python 3.x
- GitHub account
- NewsAPI account ([Get API Key](https://newsapi.org/))

#### Repository Secrets

Add the following secrets to your GitHub repository (Settings > Secrets and variables > Actions > New repository secret):

1. `SENDER_EMAIL`
2. `RECEIVER_EMAIL`
3. `EMAIL_PASSWORD`
4. `NEWS_API_KEY`

### Python Script

Ensure the Python script (`email_version/daily_report_email.py`) uses the environment variables.

**`email_version/daily_report_email.py`**:

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
        run: python email_version/daily_report_email.py
```

## Web Version

### Setup

#### Prerequisites

- Python 3.x
- GitHub Pages enabled for the repository
- NewsAPI account ([Get API Key](https://newsapi.org/))

### Files

Ensure the following files are in the `web_version` directory:

**`web_version/daily_report_web.py`**:

```python
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
```

**`web_version/index.html`**:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Daily News Report</title>
  <link rel="stylesheet" href="styles.css">
  <script src="script.js" defer></script>
</head>
<body>
  <header>
    <h1>Daily News Report</h1>
  </header>
  <main>
    <section id="report">
      <h2>Today's Report</h2>
      <div id="content">
        <!-- Report content will be inserted here -->
      </div>
    </section>
  </main>
  <footer>
    <p>For more information and custom AI solutions, visit us on <a href="https://www.linkedin.com/company/tm-hospitality-strategies/?viewAsMember=true" target="_blank">LinkedIn</a>.</p>
    <p>Powered by <a href="https://newsapi.org/" target="_blank">NewsAPI</a>.</p>
  </footer>
</body>
</html>
```

**`web_version/styles.css`**:

```css
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
}

body {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f5f5f5;
  color: #333;
}

header {
  background-color: #4CAF50;
  color: white;
  padding: 1rem;
  text-align: center;
}

main {
  flex: 1;
  padding: 2rem;
}

section#report {
  background-color: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,

 0, 0, 0.1);
}

footer {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 1rem;
}

footer a {
  color: #4CAF50;
  text-decoration: none;
}

footer a:hover {
  text-decoration: underline;
}
```

**`web_version/script.js`**:

```javascript
document.addEventListener('DOMContentLoaded', () => {
  const contentDiv = document.getElementById('content');

  fetch('report.json')
    .then(response => response.json())
    .then(data => {
      contentDiv.innerHTML = `
        <h3>AI News</h3>
        <p>${data.ai_news}</p>
        <h3>Stock Market News</h3>
        <p>${data.stock_news}</p>
        <h3>Crypto News</h3>
        <p>${data.crypto_news}</p>
      `;
    })
    .catch(error => {
      contentDiv.innerHTML = `<p>Failed to load the report: ${error}</p>`;
    });
});
```

### Running the Script

Run the Python script to generate the `report.json` file:

```sh
python web_version/daily_report_web.py
```

### GitHub Pages

Ensure GitHub Pages is enabled in your repository settings and points to the `web_version` directory.

## License

This project is licensed under the MIT License.

---

For more information and custom AI solutions, visit us on [LinkedIn](https://www.linkedin.com/company/tm-hospitality-strategies/?viewAsMember=true).

[![Visit TM Hospitality Strategies on LinkedIn](https://img.shields.io/badge/Visit%20Us%20on-LinkedIn-blue?logo=linkedin)](https://www.linkedin.com/company/tm-hospitality-strategies/?viewAsMember=true)
[![Powered by NewsAPI](https://img.shields.io/badge/Powered%20by-NewsAPI-red?logo=newsapi)](https://newsapi.org/)
```
