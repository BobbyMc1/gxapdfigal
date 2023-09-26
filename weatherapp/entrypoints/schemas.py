from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel


class Entry(BaseModel):
    temperature: float | None = None
    humidity: float | None = None
    wind_speed: float | None = None
    location: str
    date_and_time: datetime


class WeatherLocation(BaseModel):
    reference: str
    location: str
