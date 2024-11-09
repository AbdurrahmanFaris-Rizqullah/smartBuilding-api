from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Monitoring(Base):
    __tablename__ = "monitoring"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(TIMESTAMP, nullable=False)
    people = Column(Integer, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    light_intensity = Column(Float, nullable=False)
    noise = Column(Float, nullable=False)
    co2 = Column(Float, nullable=False)
    pm25 = Column(Float, nullable=False)
    airflow = Column(Float, nullable=False)
    energy = Column(Float)
    cost = Column(Float)
    comfort = Column(Float)

class MonitoringData(BaseModel):
    timestamp: str
    people: int
    temperature: float
    humidity: float
    light_intensity: float
    noise: float
    co2: float
    pm25: float
    airflow: float
    energy: Optional[float] = None
    cost: Optional[float] = None
    comfort: Optional[float] = None

    class Config:
        from_attributes = True

