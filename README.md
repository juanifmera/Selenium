# 🤖 Dollar Tweet Bot

A bot that scrapes dollar exchange rates from [dolarhoy.com](https://dolarhoy.com/) and automatically tweets daily updates with the latest buy/sell values for different dollar types, including Blue, Oficial, MEP, and Crypto 💸🐍

---

## 📌 What does this bot do?

- Extracts up-to-date dollar prices using **web scraping** with `BeautifulSoup`
- Formats a tweet with the latest values
- Logs into **X (formerly Twitter)** using `Selenium`
- Publishes the tweet automatically from your account
- All credentials are securely loaded from a `.env` file 🔐

---

## 🧠 Technologies used

- 🐍 Python 3.10+
- 🌐 BeautifulSoup (web scraping)
- 🛜 Requests (HTTP client)
- 📊 Pandas (data formatting)
- 🧪 Selenium (browser automation)
- 🛠️ Python-dotenv (environment config)

---

## ⚙️ Setup and installation

1. **Clone the repository**

```bash
git clone https://github.com/juanifmera/dollar-tweet-bot.git
cd dollar-tweet-bot
