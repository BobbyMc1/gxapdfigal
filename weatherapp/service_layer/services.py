from datetime import datetime

from weatherapp.adapters.repository import AbstractRepository
from weatherapp.domain import model


class InvalidLocation(Exception):
    pass


def is_valid_location(location, weather_history) -> bool:
    return location in {reading.location for reading in weather_history}


def add_weather_history(reference: str, location: str, repo: AbstractRepository, session) -> None:
    repo.add(model.WeatherHistory(reference, location))
    session.commit()


def get_sensor_date(location: str, stat: str, repo: AbstractRepository, start_date: datetime, end_date: datetime):
    [result] = repo.get_sensor_data(start_date, end_date, stat, location)
    result = result._asdict()
    return result


def update(
    temperature: float,
    humidity: float,
    wind_speed: float,
    location: str,
    date_and_time: datetime,
    repo: AbstractRepository,
    session,
) -> str:
    entry = model.SensorEntry(temperature, humidity, wind_speed, location, date_and_time)
    weather_readings = repo.list()
    if not is_valid_location(entry.location, weather_readings):
        raise InvalidLocation(f"Invalid location{entry.location}")
    entry_ref = model.update(entry, weather_readings)
    session.commit()
    return entry_ref
