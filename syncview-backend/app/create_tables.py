import os
import sys

# 현재 경로 기준으로 app 폴더를 path에 추가 (Windows PowerShell 대응용)
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from app.database import engine
from app.models import Base

def create_all_tables():
    print("📦 테이블 생성 중...")
    Base.metadata.create_all(bind=engine)
    print("✅ 모든 테이블 생성 완료!")

if __name__ == "__main__":
    create_all_tables()
