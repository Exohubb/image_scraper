<div align="center">

# 🖼️ Image Scraper

### Google Image Search Scraper with MongoDB Storage & Azure Deployment

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=flat-square&logo=mongodb&logoColor=white)](https://mongodb.com/atlas)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup4-HTML%20Parser-orange?style=flat-square)](https://www.crummy.com/software/BeautifulSoup)
[![Azure](https://img.shields.io/badge/Deployed%20on-Azure%20App%20Service-0078D4?style=flat-square&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

**Image Scraper** is a Flask web app that lets you search any keyword and scrapes matching images from Google Image Search, saves them locally as `.jpg` files, and stores the image binary data in MongoDB Atlas for persistence.

</div>

---

## ✨ Features

- **🔍 Google Image Search** — Scrapes images from Google's image search results for any keyword
- **💾 Local File Storage** — Downloads and saves images to `images/` directory as `{query}_{index}.jpg`
- **🗄️ MongoDB Persistence** — Stores image binary data in MongoDB Atlas collection `image_scrap_data`
- **🤖 Bot Bypass** — Spoofs Chrome User-Agent header to avoid Google bot detection
- **📝 Logging** — All errors logged to `scrapper.log` for debugging
- **🌐 Web UI** — Clean search form frontend served via Jinja2 HTML templates
- **☁️ CI/CD** — GitHub Actions pipeline auto-deploys to Azure App Service on every push to `main`

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.9** | Runtime |
| **Flask** | Web framework (routes, Jinja2 templates) |
| **Flask-CORS** | Cross-Origin Resource Sharing support |
| **Requests** | HTTP client for fetching Google search page and image URLs |
| **BeautifulSoup4** | HTML parsing — extracts all `<img>` tags from the results page |
| **PyMongo** | MongoDB Atlas client for storing image binary data |
| **Jinja2** | HTML templating (base, index, result layouts) |
| **Azure App Service** | Cloud deployment (Python 3.9 runtime) |
| **GitHub Actions** | CI/CD pipeline — build, artifact upload, Azure deploy |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│                  Browser (User)                          │
│                                                          │
│  GET  /         → Search form (index.html)               │
│  POST /review   → Submit keyword                         │
└──────────────────────────┬───────────────────────────────┘
                            │
┌──────────────────────────▼───────────────────────────────┐
│              Flask App (app.py)                          │
│                                                          │
│  1. Receive keyword from form                            │
│  2. GET https://www.google.com/search?tbm=isch&q={query} │
│     with spoofed Chrome User-Agent                       │
│  3. BeautifulSoup → find all <img> tags                  │
│  4. For each image URL:                                  │
│     → requests.get(image_url) → binary content           │
│     → save to images/{query}_{index}.jpg                 │
│     → append to img_data list                            │
│  5. pymongo.insert_many(img_data) → MongoDB Atlas        │
│  6. Return "image loaded"                                │
└─────────────────┬──────────────────┬─────────────────────┘
                  │                  │
        ┌─────────▼──────┐  ┌────────▼────────────┐
        │  images/       │  │  MongoDB Atlas       │
        │  (local disk)  │  │                      │
        │                │  │  DB: image_scrap     │
        │  query_0.jpg   │  │  Collection:         │
        │  query_1.jpg   │  │  image_scrap_data    │
        │  ...           │  │  { Index, Image }    │
        └────────────────┘  └─────────────────────-┘
```

---

## 📁 Project Structure

```
image_scraper/
├── app.py                          # Flask app — routes + scraping + MongoDB logic
├── requirements.txt                # Python dependencies
├── scrapper.log                    # Error log file (auto-generated)
├── .github/
│   └── workflows/
│       └── main_imagescraper.yml  # GitHub Actions CI/CD → Azure App Service
├── static/
│   └── css/
│       ├── style.css              # Search page styles
│       └── main.css               # Global base styles
└── templates/
    ├── base.html                  # Base layout with shared HTML structure
    ├── index.html                 # Search form page (extends base)
    └── result.html                # Results page template
```

---

## 🚀 Local Development

### Prerequisites

- Python 3.9+
- A [MongoDB Atlas](https://mongodb.com/atlas) cluster (free tier works)

### 1. Clone the repo

```bash
git clone https://github.com/Exohubb/image_scraper.git
cd image_scraper
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure MongoDB connection

In `app.py`, replace the MongoDB URI with your own Atlas connection string:

```python
client = pymongo.MongoClient("mongodb+srv://<user>:<password>@<cluster>.mongodb.net/")
```

### 4. Run the app

```bash
python app.py
```

Open [http://localhost:8000](http://localhost:8000), type any keyword, and hit **Search**.

---

## ☁️ Deploying to Azure App Service

Deployment is fully automated via GitHub Actions (`.github/workflows/main_imagescraper.yml`).

**Every push to `main` triggers:**
1. Set up Python 3.9 environment
2. Install dependencies from `requirements.txt`
3. Upload build artifact
4. Login to Azure via OIDC (no stored credentials)
5. Deploy to Azure App Service `imageScraper`

### Manual setup (first time)

1. Create an **Azure App Service** (Python 3.9, Linux)
2. Add these GitHub repository secrets:
   - `AZURE_CLIENT_ID`
   - `AZURE_TENANT_ID`
   - `AZURE_SUBSCRIPTION_ID`
3. Push to `main` — GitHub Actions handles the rest

---

## 🔌 API Routes

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Renders the search form (`index.html`) |
| `POST` | `/review` | Accepts keyword, scrapes images, saves to disk + MongoDB |

---

## 📦 Dependencies

```
flask          # Web framework + Jinja2 templating
flask_cors     # CORS headers for cross-origin requests
requests       # HTTP client (Google search + image download)
bs4            # BeautifulSoup4 — HTML parser for <img> tag extraction
pymongo        # MongoDB Atlas client for image binary storage
```

---

## 📝 Logging

All exceptions are captured and written to `scrapper.log`:

```python
logging.basicConfig(filename="scrapper.log", level=logging.INFO)
```

If scraping fails (network error, blocked by Google, etc.), the error is logged and the user sees `"something is wrong"`.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first.

1. Fork the repo
2. Create your branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m 'feat: add your feature'`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
  Made with ♥ by <a href="https://github.com/Exohubb">Exohubb</a>
</div>
