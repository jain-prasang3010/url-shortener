# 🔗 URL Shortener Service

A backend service built using FastAPI that allows users to generate short URLs and seamlessly redirect to original links. Designed with scalability, performance, and clean API architecture in mind.

---

## 🚀 Features

- Generate short URLs from long links
- Fast redirection to original URLs
- RESTful API design
- Unique ID generation for each URL
- Optimized database queries for quick lookup
- Modular backend architecture

---

## 🛠 Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** SQLite / SQLAlchemy
- **Server:** Uvicorn
- **Other:** Pydantic for validation

---

## ⚙️ How It Works

1. User sends a long URL via API
2. System generates a unique short ID
3. Mapping is stored in the database
4. When short URL is accessed → redirects to original URL

---

## 📌 API Endpoints

### 🔹 Create Short URL
**POST** `/shorten`

Request:
```json
{
  "url": "https://example.com"
}
