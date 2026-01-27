# app.py
from flask import Flask
import threading, requests, json

app = Flask(__name__)

BOT_TOKEN = "8030080377:AAF4njkWZI_DbtdQJlTRPVTK2XsaaLOZ0bM"
CHAT_ID = "1282893152"

NOTICE_URL = "https://kmu.ac.bd/frontNotice"  # KMU notice page

def check_notice():
    try:
        # 1. Fetch website content (example: HTML or JSON)
        r = requests.get(NOTICE_URL)
        r.raise_for_status()
        data = r.json()  # যদি JSON এ data আসে, অন্যথায় HTML parse করতে হবে
        latest_notice = data[0]["title"]  # উদাহরণ, adapt করো site structure অনুযায়ী

        # 2. Load last notice
        try:
            with open("last.json") as f:
                last = json.load(f)
                last_notice = last.get("last_notice", "")
        except:
            last_notice = ""

        # 3. Compare
        if latest_notice != last_notice:
            text = f"📝 New KMU notice: {latest_notice}"
            # Update last notice
            with open("last.json", "w") as f:
                json.dump({"last_notice": latest_notice}, f)
        else:
            text = "❌ No new KMU notice"

        # 4. Send Telegram message
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                      data={"chat_id": CHAT_ID, "text": text})

    except Exception as e:
        print("Error checking notice:", e)

@app.route("/")
def index():
    threading.Thread(target=check_notice).start()
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
