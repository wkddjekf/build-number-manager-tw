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
) -> List[models.BuildRecord]:
    return (
        db.query(models.BuildRecord)
        .filter(models.BuildRecord.stream == stream)
        .order_by(desc(models.BuildRecord.created_at))
        .limit(limit)
        .all()
    )


def get_history_by_build(
    db: Session,
    build: str,
    limit: int = 20,
) -> List[models.BuildRecord]:
    return (
        db.query(models.BuildRecord)
        .filter(models.BuildRecord.build == build)
        .order_by(desc(models.BuildRecord.created_at))
        .limit(limit)
        .all()
    )


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
