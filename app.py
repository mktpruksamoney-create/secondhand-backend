from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def search_kaidee(keyword):
    url = f"https://www.kaidee.com/search?q={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    items = soup.select("a[data-testid='listing-card']")
    results = []

    for item in items[:12]:
        title = item.get_text(strip=True)
        link = "https://www.kaidee.com" + item.get("href")

        price_tag = item.select_one("span")
        price = price_tag.text if price_tag else "ไม่ระบุ"

        results.append({
            "title": title,
            "price": price,
            "source": "Kaidee",
            "link": link
        })

    return results

@app.route("/api/search")
def search():
    keyword = request.args.get("keyword", "")
    data = search_kaidee(keyword)
    return jsonify(data)

@app.route("/")
def home():
    return "API พร้อมใช้งาน 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
