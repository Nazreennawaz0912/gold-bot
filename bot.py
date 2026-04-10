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

    # Find 22K section
    section = soup.find("section", attrs={"data-gr-title": lambda x: x and "22 Carat Gold Price" in x})
    table = section.find("table")

    for row in table.tbody.find_all("tr"):
        cols = row.find_all("td")
        if cols[0].get_text(strip=True) == "1":
            price = cols[1].get_text(strip=True)
            return float(price.replace("₹", "").replace(",", ""))

    return None

# Run once
price = get_gold_price()

if price:
    send_telegram(f"🔔 Coimbatore Gold Price\n22K: ₹{price:,.0f}")
else:
    send_telegram("⚠️ Failed to fetch gold price")
