import abc
from datetime import datetime, timedelta
from typing import List

from sqlalchemy import func

from weatherapp.domain import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, weather_history: model.WeatherHistory):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.WeatherHistory:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, weather_history: model.WeatherHistory):
        self.session.add(weather_history)

    def get(self, reference):
        return self.session.query(model.WeatherHistory).filter_by(reference=reference).one()

    def list(self) -> List[model.WeatherHistory]:
        return self.session.query(model.WeatherHistory).all()

    def get_sensor_data(self, start_date: datetime, end_date: datetime, statistic: str, location: str):
        stats = {"avg": func.avg, "max": func.max, "min": func.min}

        if start_date is None:
            start_date = datetime.now() - timedelta(40)

        if end_date is None:
            end_date = datetime.now()

        result = (
            self.session.query(
                stats.get(statistic)(model.SensorEntry.temperature).label("temperature"),
                stats.get(statistic)(model.SensorEntry.humidity).label("humidity"),
                stats.get(statistic)(model.SensorEntry.wind_speed).label("wind_speed"),
                model.WeatherHistory.reference,
                model.WeatherHistory.location,
            )
            .join(model.WeatherHistory, model.SensorEntry.location == model.WeatherHistory.location)
            .filter(model.SensorEntry.date_and_time.between(start_date, end_date))
            .filter(model.WeatherHistory.location == location)
        )

        return result
