# app.py
from flask import Flask
import threading
import requests
import json

app = Flask(__name__)

# === HARD-CODED TOKEN & CHAT ID ===
BOT_TOKEN = "8030080377:AAF4njkWZI_DbtdQJlTRPVTK2XsaaLOZ0bM"
CHAT_ID = "1282893152"

# === FUNCTION TO CHECK NOTICE & SEND TELEGRAM MESSAGE ===
def check_notice():
    # Example: scrape notice or use last.json logic
    # For now, just a test message
    new_notice = "📝 New KMU notice detected!"
    
    # Send message to Telegram
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": new_notice})
    except Exception as e:
        print("Error sending message:", e)

# === FLASK ROUTE ===
@app.route("/")
def index():
    # Respond immediately to avoid cron timeout
    threading.Thread(target=check_notice).start()
    return "OK", 200

# === MAIN ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
