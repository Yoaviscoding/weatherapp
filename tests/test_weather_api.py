import pytest
from httpx import AsyncClient
from app.api.weather import router
from fastapi import FastAPI
import sqlite3

app = FastAPI()
app.include_router(router, prefix="/api")

def setup_database():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            localtime TEXT,
            name TEXT,
            country TEXT,
            temp_c REAL,
            condition_text TEXT
        )
    ''')
    conn.commit()
    conn.close()

@pytest.mark.asyncio
async def test_get_city_info():
    setup_database()
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO weather_data (localtime, name, country, temp_c, condition_text)
        VALUES (?, ?, ?, ?, ?)
    ''', ('2024-08-08 10:00', 'Test City', 'Test Country', 25, 'Sunny'))
    conn.commit()
    conn.close()

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/exercise/Test Country")

    assert response.status_code == 200
    assert response.json() == [
        {
            "city": "Test City",
            "average_temp_c": 25.0,
            "latest_condition_text": "Sunny"
        }
    ]

    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM weather_data WHERE name = ?', ('Test City',))
    conn.commit()
    conn.close()


@pytest.mark.asyncio
async def test_get_city_info_not_found():
    setup_database()  # Ensure the database and table are set up
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/exercise/Unknown Country")

    assert response.status_code == 404
    assert response.json() == {"detail": "Country not found"}