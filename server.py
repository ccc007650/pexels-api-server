from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")


# Home page
@app.route("/")
def home():
    return '''
    <h2>Pexels Image Search</h2>

    <form action="/search_page">
        <input type="text" name="query" placeholder="Search images..." />
        <button type="submit">Search</button>
    </form>
    '''


# Browser page route (HTML images)
@app.route("/search_page")
def search_page():

    query = request.args.get("query", "")

    url = "https://api.pexels.com/v1/search"

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    params = {
        "query": query,
        "per_page": 5
    }

    res = requests.get(url, headers=headers, params=params)

    data = res.json()

    images_html = ""

    for photo in data.get("photos", []):
        img_url = photo["src"]["medium"]

        images_html += f'''
        <img src="{img_url}" style="margin:10px;max-width:300px;">
        '''

    return f'''
    <h2>Results for "{query}"</h2>

    <a href="/">Back</a>

    <br><br>

    {images_html}
    '''


# API route for Agent Zero / scripts
@app.route("/search_pexels", methods=["POST"])
def search_pexels():

    data = request.json

    query = data.get("query", "")

    url = "https://api.pexels.com/v1/search"

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    params = {
        "query": query,
        "per_page": 5
    }

    res = requests.get(url, headers=headers, params=params)

    return jsonify(res.json())


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )