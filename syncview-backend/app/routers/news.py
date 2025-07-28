from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import News
from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.crawlers.bbc_crawler import crawl_bbc  # 함수 직접 호출

router = APIRouter(prefix="/news", tags=["news"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class NewsCreate(BaseModel):
    title: str
    content: str
    url: str
    publisher: str = ""
    category: str = ""
    published_at: datetime = None

class NewsOut(BaseModel):
    id: int
    title: str
    content: str
    url: str
    publisher: str
    category: str
    published_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True

@router.post("/", response_model=NewsOut)
def create_news(news: NewsCreate, db: Session = Depends(get_db)):
    db_news = News(**news.dict())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

@router.get("/", response_model=List[NewsOut])
def get_news_list(db: Session = Depends(get_db)):
    return db.query(News).order_by(News.created_at.desc()).all()

@router.get("/{news_id}", response_model=NewsOut)
def get_news_detail(news_id: int, db: Session = Depends(get_db)):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="뉴스를 찾을 수 없습니다.")
    return news

@router.get("/crawl-bbc")
def crawl_bbc_news():
    headlines = crawl_bbc()
    if isinstance(headlines, dict) and "error" in headlines:
        return JSONResponse(content={"error": headlines["error"]}, status_code=500)
    return JSONResponse(content={"result": headlines["headlines"]})
