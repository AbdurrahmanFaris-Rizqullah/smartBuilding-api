import sqlite3

def get_db_connection():
    conn = sqlite3.connect('monitoring.db')
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monitoring (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            people INTEGER,
            temperature REAL,
            humidity REAL,
            light_intensity REAL,
            noise REAL,
            co2 REAL,
            pm25 REAL,
            airflow REAL,
            energy REAL,
            cost REAL,
            comfort REAL
        )
    ''')
    conn.commit()
    conn.close()
