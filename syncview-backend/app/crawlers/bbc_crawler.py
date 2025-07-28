import requests
from bs4 import BeautifulSoup
from datetime import datetime
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/crawl-bbc")
def crawl_bbc(limit: int = 5):
    try:
        url = "https://www.bbc.com/news"
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        news_list = []

        for item in soup.select("a.gs-c-promo-heading")[:limit]:
            title = item.get_text(strip=True)
            link = item.get("href")
            if not link.startswith("http"):
                link = "https://www.bbc.com" + link

            news = {
                "title": title,
                "url": link,
                "content": "",
                "publisher": "BBC",
                "category": "international",
                "published_at": datetime.now().isoformat()
            }
            news_list.append(news)

        return JSONResponse(content={"headlines": news_list})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
