from fastapi import FastAPI
from api import weather
import uvicorn

app = FastAPI()

app.include_router(weather.router, prefix="/api")

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)

