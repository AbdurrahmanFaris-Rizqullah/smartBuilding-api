from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import time
import sqlite3
from app.database import get_db_connection, initialize_db
from app.models import MonitoringData
from app.utils import update_with_ml_model

app = FastAPI()

# Inisialisasi database saat aplikasi mulai
@app.on_event("startup")
def on_startup():
    initialize_db()

def update_data_every_5_seconds():
    while True:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM monitoring ORDER BY timestamp DESC LIMIT 1")
        data = cursor.fetchone()
        if data:
            data_dict = dict(data)
            updated_data = update_with_ml_model(data_dict)
            cursor.execute('''
                UPDATE monitoring SET energy = ?, comfort = ?
                WHERE id = ?
            ''', (updated_data['energy'], updated_data['comfort'], data['id']))
            conn.commit()
        time.sleep(5)
        conn.close()

@app.on_event("startup")
def start_background_tasks():
    BackgroundTasks().add_task(update_data_every_5_seconds)

@app.post("/monitoring")
async def update_monitoring(data: MonitoringData):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO monitoring (timestamp, people, temperature, humidity, light_intensity, noise, co2, pm25, airflow, energy, cost, comfort)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data.timestamp, data.people, data.temperature, data.humidity, data.light_intensity,
          data.noise, data.co2, data.pm25, data.airflow, data.energy, data.cost, data.comfort))
    conn.commit()
    conn.close()
    return {"status": "success", "data": data}

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
async def get_levels():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT cost, energy FROM monitoring ORDER BY timestamp DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    if not result:
        raise HTTPException(status_code=404, detail="No data found")
    return {"cost": result['cost'], "energy": result['energy']}

@app.get("/comfort")
async def get_comfort():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT comfort FROM monitoring ORDER BY timestamp DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    if not result:
        raise HTTPException(status_code=404, detail="No data found")
    return {"comfort": result['comfort']}
