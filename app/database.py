from sqlalchemy import create_engine, Column, Integer, Float, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID  # Import tipe UUID dari PostgreSQL dialect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid  # Import modul uuid untuk pembuatan UUID otomatis

DATABASE_URL = "postgresql://postgres:Faris123@localhost/db-smartBuilding"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Monitoring(Base):
    __tablename__ = "dataset_energy_comfort_refined2"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)  # Ubah tipe data ke UUID
    people = Column(Integer, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    lightIntensity = Column(Float, nullable=False)
    noise = Column(Float, nullable=False)
    co2 = Column(Float, nullable=False)
    pm25 = Column(Float, nullable=False)
    airflow = Column(Float, nullable=False)
    energy = Column(Float)
    comfort = Column(Float)
    datetime = Column(TIMESTAMP, nullable=False)  # Gunakan TIMESTAMP untuk datetime

def initialize_db():
    Base.metadata.create_all(bind=engine)

def get_db_connection():
    db = SessionLocal()
    return db

