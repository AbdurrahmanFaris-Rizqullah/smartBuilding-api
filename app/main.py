from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import time
import asyncio  # Import asyncio untuk asynchronous tasks
from psycopg2.extras import RealDictCursor
from app.database import get_db_connection, initialize_db
from app.ml.models_schemas import MonitoringData
from app.utils import update_with_ml_model

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    initialize_db()

async def update_data_every_5_seconds():
   async def update_data_every_5_seconds():
    while True:
        with get_db_connection() as conn:
            cursor = conn.execute("SELECT * FROM dataset_energy_comfort_refined2 ORDER BY datetime DESC LIMIT 1")
            data = cursor.fetchone()
            if data:
                updated_data = update_with_ml_model(data)
                conn.execute('''
                    UPDATE dataset_energy_comfort_refined2 SET energy = %s, comfort = %s
                    WHERE id = %s
                ''', (updated_data['energy'], updated_data['comfort'], data['id']))
                conn.commit()
        await asyncio.sleep(5)  # Menunggu 5 detik sebelum melakukan update berikutnya



@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(update_data_every_5_seconds())

@app.post("/monitoring")
async def update_monitoring(data: MonitoringData):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO dataset_energy_comfort_refined2 (datetime, people, temperature, humidity, lightIntensity, noise, co2, pm25, airflow, energy, comfort)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (data.datetime, data.people, data.temperature, data.humidity, data.lightIntensity,
          data.noise, data.co2, data.pm25, data.airflow, data.energy, data.comfort))
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
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT energy, comfort FROM dataset_energy_comfort_refined2 ORDER BY datetime DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    if not result:
        raise HTTPException(status_code=404, detail="No data found")
    return {"energy": result['energy'], "comfort": result['comfort']}

@app.get("/comfort")
async def get_comfort():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT comfort FROM dataset_energy_comfort_refined2 ORDER BY datetime DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    if not result:
        raise HTTPException(status_code=404, detail="No data found")
    return {"comfort": result['comfort']}
