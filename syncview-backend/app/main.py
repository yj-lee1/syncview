from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import news
from app.crawlers import bbc_crawler
from dotenv import load_dotenv
import os

# .env 로드
load_dotenv()

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기본 라우트
@app.get("/")
def root():
    return {"message": "Hello, SyncView"}

# 뉴스 및 크롤러 라우터 포함
app.include_router(news.router)
app.include_router(bbc_crawler.router)
