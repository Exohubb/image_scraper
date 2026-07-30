<div align="center">

# 🖼️ Image Scraper

### Google Image Search Scraper with Local Device Storage

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup4-HTML%20Parser-orange?style=flat-square)](https://www.crummy.com/software/BeautifulSoup)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

**Image Scraper** is a Flask web application that scrapes image search results from Google, automatically decodes and downloads images (supporting both HTTP/HTTPS links and Base64 Data URIs), and stores them directly on local device disk (`images/`).

</div>

---

## ✨ Features

- **🔍 Google Image Search** — Scrapes images from search results for any keyword
- **💾 Local Storage** — Saves downloaded images directly to local device directory (`images/{query}_{index}.jpg`)
- **🖼️ Image Gallery UI** — Interactive frontend grid showing image previews, indices, and download options
- **🛡️ Robust Extraction** — Handles both `http(s)` URLs and `base64` embedded data URIs cleanly
- **🤖 Bot Prevention Bypass** — Uses standard browser User-Agent headers to prevent Google blocks
- **📝 Comprehensive Logging** — Detailed exception tracking saved to `scrapper.log`

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.9+** | Runtime environment |
| **Flask** | Web framework & routes |
| **Flask-CORS** | Cross-Origin Resource Sharing |
| **Requests** | HTTP client for image fetching |
| **BeautifulSoup4** | HTML parsing for `<img>` tag extraction |
| **Jinja2** | HTML templating for web UI |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│                  Browser (User)                          │
│                                                          │
│  GET  /         → Search form (index.html)               │
│  POST /review   → Submit keyword                         │
│  GET  /images/* → Serve local images                     │
└──────────────────────────┬───────────────────────────────┘
                            │
┌──────────────────────────▼───────────────────────────────┐
│              Flask App (app.py)                          │
│                                                          │
│  1. Receive keyword from form                            │
│  2. GET Google Image search with Chrome User-Agent       │
│  3. BeautifulSoup → parse <img> src & data-src tags      │
│  4. For each image URL / base64 data URI:                │
│     → Decode base64 or fetch binary stream               │
│     → Save to images/{query}_{index}.jpg on local disk   │
│  5. Render result.html image gallery UI                    │
└──────────────────────────┬───────────────────────────────┘
                            │
                  ┌─────────▼──────┐
                  │  images/       │
                  │  (local disk)  │
                  │                │
                  │  cat_0.jpg     │
                  │  cat_1.jpg     │
                  │  ...           │
                  └────────────────┘
```

---

## 🚀 Local Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the application

```bash
python app.py
```

Open [http://localhost:8000](http://localhost:8000), enter any keyword, and click **Scrape & Save Images**. Scraped images will automatically save to the `images/` directory on your device.

---

## 🔌 API Routes

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Renders search form (`index.html`) |
| `POST` | `/review` | Accepts search query, scrapes images, saves to `images/` folder, and renders result page |
| `GET` | `/images/<filename>` | Serves locally saved images to browser |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
