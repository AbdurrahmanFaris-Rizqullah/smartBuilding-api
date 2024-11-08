from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, initialize_db
from app.models_schemas import Monitoring, MonitoringData
from app.utils import update_with_ml_model
import time

app = FastAPI()

# Inisialisasi database saat aplikasi mulai
@app.on_event("startup")
def on_startup():
    initialize_db()
    BackgroundTasks().add_task(update_data_every_5_seconds)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def update_data_every_5_seconds():
    while True:
        db = next(get_db())
        data = db.query(Monitoring).order_by(Monitoring.timestamp.desc()).first()
        if data:
            data_dict = {
                'timestamp': data.timestamp,
                'people': data.people,
                'temperature': data.temperature,
                'humidity': data.humidity,
                'light_intensity': data.light_intensity,
                'noise': data.noise,
                'co2': data.co2,
                'pm25': data.pm25,
                'airflow': data.airflow,
                'energy': data.energy,
                'cost': data.cost,
                'comfort': data.comfort
            }
            updated_data = update_with_ml_model(data_dict)
            data.energy = updated_data['energy']
            data.comfort = updated_data['comfort']
            db.commit()
        time.sleep(5)

@app.post("/monitoring")
async def update_monitoring(data: MonitoringData, db: Session = Depends(get_db)):
    new_entry = Monitoring(**data.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return {"status": "success", "data": new_entry}

@app.post("/custom-scenario")
async def custom_scenario(data: MonitoringData):
    updated_data = update_with_ml_model(data.dict())
    return {"status": "success", "data": updated_data}

@app.post("/mode-scenario")
async def mode_scenario(mode: str):
    # Terapkan skenario yang dipilih dan perbarui data menggunakan model machine learning
    updated_data = {}
    return {"status": "success", "data": updated_data}

@app.get("/levels")
async def get_levels(db: Session = Depends(get_db)):
    result = db.query(Monitoring.cost, Monitoring.energy).order_by(Monitoring.timestamp.desc()).first()
    if not result:
        raise HTTPException(status_code=404, detail="No data found")
    return {"cost": result.cost, "energy": result.energy}

@app.get("/comfort")
async def get_comfort(db: Session = Depends(get_db)):
    result = db.query(Monitoring.comfort).order_by(Monitoring.timestamp.desc()).first()
    if not result:
        raise HTTPException(status_code=404, detail="No data found")
    return {"comfort": result.comfort}
