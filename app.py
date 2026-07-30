import os
import re
import json
import base64
import logging
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

logging.basicConfig(
    filename="scrapper.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

app = Flask(__name__)
CORS(app)

SAVE_DIRECTORY = "images"

if not os.path.exists(SAVE_DIRECTORY):
    os.makedirs(SAVE_DIRECTORY)

def fetch_image_urls(query):
    """Scrapes image URLs from multiple search providers for maximum reliability."""
    urls = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    # 1. Bing Image Search (High quality murl extraction + img tags)
    try:
        bing_url = f"https://www.bing.com/images/search?q={requests.utils.quote(query)}"
        res = requests.get(bing_url, headers=headers, timeout=8)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "html.parser")
            
            # Extract high-res murl links
            for a in soup.find_all("a", class_="iusc"):
                m = a.get("m")
                if m:
                    try:
                        m_data = json.loads(m)
                        if "murl" in m_data and m_data["murl"]:
                            urls.append(m_data["murl"])
                    except Exception:
                        pass
            
            # Extract img src and data-src tags
            for img in soup.find_all("img"):
                src = img.get("src") or img.get("data-src") or img.get("src2")
                if src and (src.startswith("http") or src.startswith("data:image/")):
                    if "r.bing.com" not in src and "svg" not in src:
                        urls.append(src)
    except Exception as e:
        logging.error(f"Error fetching Bing images for '{query}': {e}")

    # 2. Google Image Search fallback
    if len(urls) < 5:
        try:
            google_url = f"https://www.google.com/search?q={requests.utils.quote(query)}&tbm=isch"
            res = requests.get(google_url, headers=headers, timeout=8)
            if res.status_code == 200:
                soup = BeautifulSoup(res.content, "html.parser")
                for img in soup.find_all("img"):
                    src = img.get("src") or img.get("data-src")
                    if src and (src.startswith("http") or src.startswith("data:image/")):
                        if "googlelogo" not in src and "1x1" not in src:
                            urls.append(src)
        except Exception as e:
            logging.error(f"Error fetching Google images for '{query}': {e}")

    return urls

@app.route("/", methods=['GET'])
def homepage():
    return render_template("index.html")

@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory(SAVE_DIRECTORY, filename)

@app.route("/review", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            raw_query = request.form.get('content', '').strip()
            if not raw_query:
                return render_template('result.html', images=[], query="N/A", error="Please enter a search keyword.")

            safe_query = re.sub(r'[^a-zA-Z0-9_-]', '_', raw_query)
            image_urls = fetch_image_urls(raw_query)

            if not image_urls:
                return render_template('result.html', images=[], query=raw_query, error="No images found for this search keyword.")

            saved_images = []
            img_index = 0
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

            for url in image_urls:
                if img_index >= 12: # Save top 12 images locally
                    break

                try:
                    image_data = None
                    file_ext = ".jpg"

                    if url.startswith("data:image/"):
                        # Handle base64 encoded data URIs
                        header, encoded = url.split(",", 1)
                        if "png" in header:
                            file_ext = ".png"
                        elif "gif" in header:
                            file_ext = ".gif"
                        elif "webp" in header:
                            file_ext = ".webp"
                        image_data = base64.b64decode(encoded)
                    elif url.startswith("http://") or url.startswith("https://"):
                        # Fetch HTTP/HTTPS image URL
                        img_res = requests.get(url, headers=headers, timeout=3)
                        if img_res.status_code == 200 and len(img_res.content) > 300:
                            image_data = img_res.content
                            # Infer extension if possible
                            content_type = img_res.headers.get("Content-Type", "")
                            if "png" in content_type:
                                file_ext = ".png"
                            elif "gif" in content_type:
                                file_ext = ".gif"
                            elif "webp" in content_type:
                                file_ext = ".webp"

                    if image_data:
                        filename = f"{safe_query}_{img_index}{file_ext}"
                        file_path = os.path.join(SAVE_DIRECTORY, filename)

                        with open(file_path, "wb") as f:
                            f.write(image_data)

                        saved_images.append({
                            "index": img_index + 1,
                            "filename": filename,
                            "url": f"/images/{filename}"
                        })
                        img_index += 1

                except Exception as img_err:
                    logging.warning(f"Skipping failed image download '{url[:50]}...': {img_err}")
                    continue

            if not saved_images:
                return render_template('result.html', images=[], query=raw_query, error="Could not save images locally.")

            return render_template('result.html', images=saved_images, query=raw_query)

        except Exception as e:
            logging.exception(f"Scraping error for request: {e}")
            return render_template('result.html', images=[], query="", error=f"An error occurred: {str(e)}")

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
