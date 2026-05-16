from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from .database import Base

class AgriculturalLog(Base):
    __tablename__ = "agricultural_logs"

    id = Column(Integer, primary_key=True, index=True)
    crop = Column(String, nullable=True)
    quantity = Column(String, nullable=True)
    location = Column(String, nullable=True)
    intent = Column(String, nullable=True)
    source = Column(String)  # 'whatsapp' or 'ussd'
    timestamp = Column(DateTime, default=datetime.utcnow)

class CrisisMetric(Base):
    __tablename__ = "crisis_metrics"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    safety_status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
