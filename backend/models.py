# backend/models.py
from sqlalchemy import Column, Integer, String, DateTime, Date, func
from .database import Base

class BuildRecord(Base):
    __tablename__ = "build_records"

    id = Column(Integer, primary_key=True, index=True)

    # Stream: LiveHotfixTW / StageTW / L10NTW
    stream = Column(String, index=True)

    # Build: LiveTW / StageTW / L10NTW
    build = Column(String, index=True)

    # BuildType: Full Build / DataOnly / DLC
    build_type = Column(String, index=True)

    version = Column(String, index=True)
    aos_version = Column(String)
    ios_version = Column(String)
    cv = Column(String)

    # 페이지에 새로 추가한 "타겟 업데이트 일자"
    # 프론트에서 YYYY-MM-DD 로 들어오면 Date 으로 잘 들어감
    target_update_date = Column(Date, nullable=True)

    created_at = Column(
        DateTime(timezone=False),
        server_default=func.now(),
        index=True,
    )
