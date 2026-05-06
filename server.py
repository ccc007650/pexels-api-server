from flask import Flask, request
import requests

app = Flask(__name__)

import os
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

@app.route("/")
def home():
    return '''
    <h2>Pexels Image Search</h2>
    <form action="/search_page">
        <input type="text" name="query" placeholder="Search images..." />
        <button type="submit">Search</button>
    </form>
    '''

@app.route("/search_page")
def search_page():
    query = request.args.get("query", "")

    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 5}

    res = requests.get(url, headers=headers, params=params)
    data = res.json()

    images_html = ""
    for photo in data.get("photos", []):
        img_url = photo["src"]["medium"]
        images_html += f'<img src="{img_url}" style="margin:10px;">'

    return f'''
    <h2>Results for "{query}"</h2>
    <a href="/">Back</a><br><br>
    {images_html}
    '''

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))