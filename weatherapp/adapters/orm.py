from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import registry, relationship

from weatherapp.domain import model

mapper_registry = registry()

metadata = mapper_registry.metadata

sensor_entries = Table(
    "sensor_entries",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("temperature", Float),
    Column("humidity", Float),
    Column("wind_speed", Float),
    Column("location", String(255), nullable=False),
    Column("date_and_time", DateTime, nullable=False),
)

weather_history = Table(
    "weather_history",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255), nullable=False),
    Column("location", String(255), nullable=False),
)

history = Table(
    "history",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sensorentry_id", ForeignKey("sensor_entries.id")),
    Column("weatherhistory_id", ForeignKey("weather_history.id")),
)


def start_mappers():
    entries_mapper = mapper_registry.map_imperatively(model.SensorEntry, sensor_entries)
    mapper_registry.map_imperatively(
        model.WeatherHistory,
        weather_history,
        properties={
            "_history": relationship(
                entries_mapper,
                secondary=history,
                collection_class=set,
            )
        },
    )
