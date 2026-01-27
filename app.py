from flask import Flask
import requests
from bs4 import BeautifulSoup
import json

# Sifu, আপনার token এবং chat ID সরাসরি বসানো হলো
import os
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
URL = "https://kmu.ac.bd/frontNotice"

app = Flask(__name__)

def send(msg):
    api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(api, data={"chat_id": CHAT_ID, "text": msg})

@app.route("/")
def check():
    r = requests.get(URL, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    notice = soup.select_one(".notice-title a")
    if not notice:
        return "No notices found"

    title = notice.text.strip()
    link = notice["href"]

    try:
        old = json.load(open("last.json"))
    except:
        old = {"title": ""}

    if title != old["title"]:
        send(f"📢 New KMU Notice:\n{title}\n{link}")
        json.dump({"title": title}, open("last.json","w"))

    return "OK"

if __name__ == "__main__":
    app.run()
