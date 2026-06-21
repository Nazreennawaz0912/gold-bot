import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.goodreturns.in/gold-rates/coimbatore.html"

TOKEN = os.environ["BOT_TOKEN"]
GROUP_CHAT_ID = os.environ["GROUP_CHAT_ID"]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": GROUP_CHAT_ID, "text": msg})
    
#send_telegram("Test message from bot ✅")

def get_gold_price():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers, timeout=10)

    soup = BeautifulSoup(r.text, "html.parser")

    tables = soup.find_all("table")

    if not tables:
        return None

    table = tables[0]

    for row in table.find_all("tr"):
        cols = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]

        # First row containing 1 gram price
        if len(cols) >= 3 and cols[0] == "1":
            price = cols[2]  # 22K column
            return float(price.replace("₹", "").replace(",", ""))

    return None

# Run once
price = get_gold_price()

if price:
    send_telegram(f"🔔 Coimbatore Gold Price\n22K: ₹{price:,.0f}")
else:
    send_telegram("⚠️ Gold price section not found on website")
