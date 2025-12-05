# backend/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles   # ★ 추가됨
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, Base
from . import models, crud
from datetime import datetime

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Build Number Manager (TW)")

# CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────
# 의존성
# ─────────────────────────────

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ─────────────────────────────
# Pydantic 모델
# ─────────────────────────────

class BuildCreate(BaseModel):
    stream: str
    build: str
    build_type: str
    version: str
    aos_version: str
    ios_version: str
    cv: str

class BuildOut(BaseModel):
    id: int
    stream: str
    build: str
    build_type: str
    version: str
    aos_version: Optional[str]
    ios_version: Optional[str]
    cv: Optional[str]
    created_at: datetime
    model_config = {"from_attributes": True}

# ─────────────────────────────
# 건강 체크
# ─────────────────────────────
@app.get("/ping")
def ping():
    return {"status": "ok"}

# ─────────────────────────────
# 최신 빌드 - Stream 기준
# ─────────────────────────────
@app.get("/latest/stream/{stream_name}", response_model=Optional[BuildOut])
def latest_by_stream(stream_name: str, db: Session = Depends(get_db)):
    return crud.get_latest_by_stream(db, stream_name)

# ─────────────────────────────
# 최신 빌드 - Build 기준
# ─────────────────────────────
@app.get("/latest/build/{build_name}", response_model=Optional[BuildOut])
def latest_by_build(build_name: str, db: Session = Depends(get_db)):
    return crud.get_latest_by_build(db, build_name)

# ─────────────────────────────
# 히스토리 - Stream 기준
# ─────────────────────────────
@app.get("/history/stream/{stream_name}", response_model=List[BuildOut])
def history_by_stream(stream_name: str, db: Session = Depends(get_db)):
    return crud.get_history_by_stream(db, stream_name)

# ─────────────────────────────
# 히스토리 - Build 기준
# ─────────────────────────────
@app.get("/history/build/{build_name}", response_model=List[BuildOut])
def history_by_build(build_name: str, db: Session = Depends(get_db)):
    return crud.get_history_by_build(db, build_name)

# ─────────────────────────────
# 빌드 등록
# ─────────────────────────────
@app.post("/build/register", response_model=BuildOut)
def register_build(payload: BuildCreate, db: Session = Depends(get_db)):
    return crud.create_build(
        db,
        stream=payload.stream,
        build=payload.build,
        build_type=payload.build_type,
        version=payload.version,
        aos_version=payload.aos_version,
        ios_version=payload.ios_version,
        cv=payload.cv,
    )

# ─────────────────────────────
# 빌드 삭제
# ─────────────────────────────
@app.delete("/build/{build_id}")
def delete_build(build_id: int, db: Session = Depends(get_db)):
    success = crud.delete_build(db, build_id)
    if not success:
        raise HTTPException(status_code=404, detail="Build record not found")
    return {"ok": True}


# =====================================================
#  ★★ 여기가 핵심: 프론트엔드 정적파일 마운트 ★★
# =====================================================
app.mount(
    "/",  # 루트 URL
    StaticFiles(directory="frontend", html=True),
    name="frontend",
)
