from flask import Flask, request, render_template
import requests

app = Flask(__name__)

API_KEY = "4e7ab31ea70dbad2863764144216327a"

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None

    # =========================
    # ★① POST（検索）
    # =========================
    if request.method == "POST":
        city = request.form.get("city")

        # ★空チェック
        if not city:
            return render_template("index.html", weather="都市名を入力してください")

        # ★ここにURLを書く（←外に出さない！）
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ja"
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

    # =========================
    # ★② GET（現在地）
    # =========================
    else:
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

    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(debug=True)