import os

from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter()

# Connect to the SQLite database
def get_db_connection():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'weather_data.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/")
def read_root():
    return {"message": "api server is up!"}

@router.get("/exercise/{location_country}")
def get_city_info(location_country: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    location_country = location_country.title()

    cursor.execute('''
        SELECT name, AVG(temp_c) as average_temp_c, condition_text
        FROM weather_data
        WHERE country = ?
        GROUP BY name
    ''', (location_country,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="Country not found")

    result = []
    for row in rows:
        result.append({
            "city": row["name"],
            "average_temp_c": row["average_temp_c"],
            "latest_condition_text": row["condition_text"]
        })

    return result