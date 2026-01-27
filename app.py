from flask import Flask
import threading
import time
import requests
from bs4 import BeautifulSoup
import telegram

app = Flask(__name__)

BOT_TOKEN = "8030080377:AAF4njkWZI_DbtdQJlTRPVTK2XsaaLOZ0bM"
CHAT_ID = 1282893152
NOTICE_URL = "https://kmu.ac.bd/frontNotice"

bot = telegram.Bot(token=BOT_TOKEN)
last_notice = ""

def fetch_latest_notice():
    """
    Fetches latest notice title from KMU notice page.
    Scrapes HTML to get the first listed notice title.
    """
    try:
        r = requests.get(NOTICE_URL, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        # Select the first notice title text
        notice_tag = soup.select_one("table tbody tr td:nth-child(3)")  # adjust selector if needed
        if notice_tag:
            return notice_tag.get_text(strip=True)
        return ""
    except Exception as e:
        print("Error fetching website:", e)
        return ""

def check_loop():
    global last_notice
    while True:
        latest = fetch_latest_notice()

        if latest and latest != last_notice:
            # New notice detected
            last_notice = latest
            message = f"📝 New KMU Notice:\n{latest}"
            # Send 20 repeated messages
            for i in range(20):
                bot.send_message(chat_id=CHAT_ID, text=message + f"\n({i+1}/20)")
                time.sleep(1)  # small delay between repeats
        else:
            bot.send_message(chat_id=CHAT_ID, text="❌ No new notice")

        # Sleep before next iteration
        time.sleep(60)

@app.route("/")
def home():
    return "KMU Bot is running 🚀", 200

if __name__ == "__main__":
    # Start background loop thread
    thread = threading.Thread(target=check_loop)
    thread.daemon = True
    thread.start()
    app.run(host="0.0.0.0", port=5000)
