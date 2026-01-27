import os
import threading, requests, json
from flask import Flask

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def check_notice():
    new_notice = "New KMU notice"  # Example
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": new_notice})

@app.route("/")
def index():
    threading.Thread(target=check_notice).start()
    return "OK", 200

if __name__ == "__main__":
    app.run()
