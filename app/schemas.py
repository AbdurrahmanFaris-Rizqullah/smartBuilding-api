from pydantic import BaseModel
from typing import Optional

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
        orm_mode = True
