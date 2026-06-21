import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.goodreturns.in/gold-rates/coimbatore.html"

TOKEN = os.environ["BOT_TOKEN"]
GROUP_CHAT_ID = os.environ["GROUP_CHAT_ID"]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": GROUP_CHAT_ID, "text": msg})
    
send_telegram("Test message from bot ✅")

def get_gold_price():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers, timeout=10)

    soup = BeautifulSoup(r.text, "html.parser")

    print("Status Code:", r.status_code)
    print("Page Title:", soup.title)

    with open("debug.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    
    # Find 22K section
    tables = soup.find_all("table")

    print("Tables found:", len(tables))

    for i, table in enumerate(tables[:5]):
        print(f"\n--- TABLE {i} ---")
        print(table.get_text(" ", strip=True)[:500])

    return None

# Run once
price = get_gold_price()

if price:
    send_telegram(f"🔔 Coimbatore Gold Price\n22K: ₹{price:,.0f}")
else:
    send_telegram("⚠️ Gold price section not found on website")
