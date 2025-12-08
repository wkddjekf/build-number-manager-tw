# backend/models.py
from sqlalchemy import Column, Integer, String, DateTime, func
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
    created_at = Column(DateTime(timezone=False), server_default=func.now(), index=True)

    
