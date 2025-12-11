# backend/crud.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import date

from . import models


def get_latest_by_stream(db: Session, stream: str) -> Optional[models.BuildRecord]:
    return (
        db.query(models.BuildRecord)
        .filter(models.BuildRecord.stream == stream)
        .order_by(desc(models.BuildRecord.created_at))
        .first()
    )


def get_latest_by_build(db: Session, build: str) -> Optional[models.BuildRecord]:
    return (
        db.query(models.BuildRecord)
        .filter(models.BuildRecord.build == build)
        .order_by(desc(models.BuildRecord.created_at))
        .first()
    )


def get_history_by_stream(
    db: Session,
    stream: str,
    limit: int = 20,
    offset: int = 0,
) -> List[models.BuildRecord]:
    """
    특정 Stream의 히스토리를 최신순으로 가져온다.
    - limit : 한 번에 가져올 최대 개수
    - offset: 건너뛸 개수 (페이징용)
    """
    query = (
        db.query(models.BuildRecord)
        .filter(models.BuildRecord.stream == stream)
        .order_by(desc(models.BuildRecord.created_at))
    )

    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)

    return query.all()


def get_history_by_build(
    db: Session,
    build: str,
    limit: int = 20,
    offset: int = 0,
) -> List[models.BuildRecord]:
    """
    특정 Build(LiveTW, StageTW 등)의 히스토리를 최신순으로 가져온다.
    """
    query = (
        db.query(models.BuildRecord)
        .filter(models.BuildRecord.build == build)
        .order_by(desc(models.BuildRecord.created_at))
    )

    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)

    return query.all()


def create_build(
    db: Session,
    *,
    stream: str,
    build: str,
    build_type: str,
    version: str,
    aos_version: str,
    ios_version: str,
    cv: str,
    target_update_date: Optional[date] = None,
) -> models.BuildRecord:
    record = models.BuildRecord(
        stream=stream,
        build=build,
        build_type=build_type,
        version=version,
        aos_version=aos_version,
        ios_version=ios_version,
        cv=cv,
        target_update_date=target_update_date,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def delete_build(db: Session, build_id: int) -> bool:
    obj = db.query(models.BuildRecord).filter(models.BuildRecord.id == build_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
