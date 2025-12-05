# backend/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv   # ★ .env 파일 로드

# ────────────────────────────────
# .env 파일 로드 (로컬 전용)
# ────────────────────────────────
load_dotenv()

# ────────────────────────────────
# Render / Local 환경변수 읽기
# ────────────────────────────────
DATABASE_URL = os.getenv("NEON_DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "❌ 환경변수 NEON_DATABASE_URL 이 설정되어 있지 않습니다.\n"
        ".env 파일 또는 Render Environment Variables 를 확인하세요."
    )

# ────────────────────────────────
# SQLAlchemy 엔진 생성
# ────────────────────────────────
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# ────────────────────────────────
# 세션 팩토리
# ────────────────────────────────
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ────────────────────────────────
# 모델 Base
# ────────────────────────────────
Base = declarative_base()
