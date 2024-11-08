from sqlalchemy import create_engine, Column, Integer, String, Float, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:Faris123@localhost/db-smartBulding"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
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

def initialize_db():
    Base.metadata.create_all(bind=engine)