from flask import Flask, request, render_template
import requests

from googletrans import Translator

app = Flask(__name__)

translator = Translator()

API_KEY = "4e7ab31ea70dbad2863764144216327a"

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None

    # ★現在地（GET）
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if lat and lon:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=ja"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            weather = "現在地の天気が取得できません"
        else:
            weather = {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "desc": data["weather"][0]["description"]
            }

    # ★都市検索（POST）
    elif request.method == "POST":
        # 日本語 → 英語に翻訳
        translated = translator.translate(city, src="ja", dest="en")
        city_en = translated.text

        url = furl = f"https://api.openweathermap.org/data/2.5/weather?q={city_en}&appid={API_KEY}&units=metric&lang=ja"
        response = requests.get(url)
        data = response.json()
        
        if data.get("cod") != 200:
            weather = "都市が見つかりません"
        else:
            weather = {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "desc": data["weather"][0]["description"]
            }

    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(debug=True)