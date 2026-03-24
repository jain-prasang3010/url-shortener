# 🔗 URL Shortener Service

A scalable backend service built using FastAPI that allows users to generate short URLs and seamlessly redirect to original links. Designed with clean API architecture, validation, and performance in mind.

---

## 🚀 Features

- Generate short URLs from long links
- Custom short code support
- Fast redirection to original URLs
- Expiry-based URL handling
- Click tracking (analytics)
- RESTful API design
- Optimized database queries
- Modular backend architecture

---

## 🛠 Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** SQLite (SQLAlchemy ORM)
- **Server:** Uvicorn
- **Validation:** Pydantic

---

## ⚙️ How It Works

1. User sends a long URL via API
2. System generates a unique short code (or uses custom code)
3. URL mapping is stored in the database
4. When short URL is accessed → redirects to original URL
5. Click count is tracked for analytics

---

## 📌 API Endpoints

### 🔹 Create Short URL
**POST** `/shorten`

Request:
```json
{
  "long_url": "https://example.com"
}
