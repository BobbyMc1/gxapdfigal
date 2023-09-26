from __future__ import annotations

from datetime import datetime
from typing import Literal

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from weatherapp.adapters import orm, repository
from weatherapp.domain import model
from weatherapp.entrypoints import schemas
from weatherapp.service_layer import services

orm.start_mappers()
get_session = sessionmaker(
    bind=create_engine("sqlite:///foo.db", connect_args={"check_same_thread": False}, echo=True),
    autocommit=False,
    autoflush=False,
)
app = FastAPI()


@app.get("/sensor-data", status_code=200)
async def get_sensor_data(
    location: str,
    statistic: Literal["min", "max", "avg"],
    start_date: datetime | None = None,
    end_date: datetime | None = None,
):
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    data = services.get_sensor_date(location, statistic, repo, start_date, end_date)

    return {"response": data}


@app.post("/locations", status_code=201)
async def add_location(log: schemas.WeatherLocation):
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    services.add_weather_history(
        log.reference,
        log.location,
        repo,
        session,
    )

    return "OK"


@app.post("/sensor-entries", status_code=201)
async def update_entry(reading: schemas.Entry):
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    try:
        sensorref = services.update(
            reading.temperature,
            reading.humidity,
            reading.wind_speed,
            reading.location,
            reading.date_and_time,
            repo,
            session,
        )

    except (model.InvalidWeatherLocation, services.InvalidLocation) as e:
        raise HTTPException(400, str(e))
    return {"sensorref": sensorref}


@app.get("/")
async def hello_word():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    __spec__ = None
    uvicorn.run("fastapi_app:app", host="0.0.0.0", port=8000, reload=True, debug=True)
