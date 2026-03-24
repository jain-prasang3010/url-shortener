from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, HttpUrl
from fastapi.responses import RedirectResponse

import random
import string
import os
import logging
from datetime import datetime, timedelta

from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# ------------------ CONFIG ------------------

DATABASE_URL = "sqlite:///./test.db"
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

logging.basicConfig(level=logging.INFO)

# ------------------ DATABASE SETUP ------------------

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

# ------------------ MODEL ------------------

class URL(Base):
    __tablename__ = "urls"

    short_code = Column(String, primary_key=True, index=True)
    long_url = Column(String, nullable=False, index=True)
    clicks = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

Base.metadata.create_all(bind=engine)

# ------------------ APP ------------------

app = FastAPI(title="URL Shortener API 🚀")

# ------------------ DB DEPENDENCY ------------------
@app.head("/")
def head_home():
    return {}
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------ UTIL ------------------

def generate_short_code(db: Session, length=6):
    characters = string.ascii_letters + string.digits

    while True:
        short_code = ''.join(random.choice(characters) for _ in range(length))
        existing = db.query(URL).filter(URL.short_code == short_code).first()
        if not existing:
            return short_code

# ------------------ SCHEMAS ------------------

class URLRequest(BaseModel):
    long_url: HttpUrl
    custom_code: str | None = None
    expires_in_days: int | None = None

class URLResponse(BaseModel):
    short_url: str

# ------------------ ROUTES ------------------

@app.get("/")
def home():
    return {"status": "success", "message": "URL Shortener Running 🚀"}

# ------------------ SHORTEN ------------------

@app.post("/shorten", response_model=URLResponse)
def shorten_url(request: URLRequest, db: Session = Depends(get_db)):

    # Validate custom code
    if request.custom_code:
        if not request.custom_code.isalnum():
            raise HTTPException(status_code=400, detail="Custom code must be alphanumeric")

    # Check if URL already exists (only if no custom code)
    existing_url = db.query(URL).filter(URL.long_url == str(request.long_url)).first()
    if existing_url and not request.custom_code:
        return {"short_url": f"{BASE_URL}/{existing_url.short_code}"}

    # Handle custom code
    if request.custom_code:
        existing = db.query(URL).filter(URL.short_code == request.custom_code).first()
        if existing:
            raise HTTPException(status_code=400, detail="Custom code already taken")
        short_code = request.custom_code
    else:
        short_code = generate_short_code(db)

    # Expiry logic
    expires_at = None
    if request.expires_in_days:
        expires_at = datetime.utcnow() + timedelta(days=request.expires_in_days)

    new_url = URL(
        short_code=short_code,
        long_url=str(request.long_url),
        clicks=0,
        expires_at=expires_at
    )

    try:
        db.add(new_url)
        db.commit()
        logging.info(f"Short URL created: {short_code}")
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

    return {"short_url": f"{BASE_URL}/{short_code}"}

# ------------------ REDIRECT ------------------

@app.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):

    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    if url.expires_at and datetime.utcnow() > url.expires_at:
        raise HTTPException(status_code=410, detail="URL expired")

    try:
        url.clicks += 1
        db.commit()
    except:
        db.rollback()

    return RedirectResponse(url.long_url)

# ------------------ ANALYTICS ------------------

@app.get("/analytics/{short_code}")
def get_analytics(short_code: str, db: Session = Depends(get_db)):

    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="Not found")

    return {
        "status": "success",
        "data": {
            "short_code": url.short_code,
            "long_url": url.long_url,
            "clicks": url.clicks,
            "created_at": url.created_at,
            "expires_at": url.expires_at
        }
    }
