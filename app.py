from flask import Flask
import threading
import time
import requests
import telegram

app = Flask(__name__)

# Your bot credentials
BOT_TOKEN = "8030080377:AAF4njkWZI_DbtdQJlTRPVTK2XsaaLOZ0bM"
CHAT_ID = 1282893152

bot = telegram.Bot(token=BOT_TOKEN)
NOTICE_URL = "https://kmu.ac.bd/frontNotice"
last_notice = None

def check_notice_loop():
    global last_notice
    while True:
        try:
            r = requests.get(NOTICE_URL, timeout=10)
            r.raise_for_status()
            notices = r.text  # simple scraping, adjust if needed
            if notices != last_notice:
                last_notice = notices
                for _ in range(20):
                    bot.send_message(chat_id=CHAT_ID, text=f"New KMU notice detected!\n{last_notice}")
                print("New notice sent 20 times ✅")
            else:
                bot.send_message(chat_id=CHAT_ID, text="No new notice ❌")
                print("No new notice ❌")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(60)

@app.route("/")
def home():
    return "KMU Bot is running!"

if __name__ == "__main__":
    threading.Thread(target=check_notice_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
