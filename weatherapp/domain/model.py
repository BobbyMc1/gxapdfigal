from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Set


class InvalidWeatherLocation(Exception):
    pass


def update(entry: SensorEntry, logs: List[WeatherHistory]) -> str:
    try:
        log = next(l for l in logs if l.can_update(entry))
        log.update(entry)
        return log.reference
    except StopIteration:
        raise (InvalidWeatherLocation(f"Invalid sensor entry for location{entry}"))


@dataclass(unsafe_hash=True)
class SensorEntry:
    temperature: float
    humidity: float
    wind_speed: float
    location: str
    date_and_time: datetime


class WeatherHistory:
    def __init__(self, reference: str, location: str):
        self.reference: str = reference
        self.location: str = location
        self._history: Set[SensorEntry] = set()

    def update(self, entry: SensorEntry) -> None:
        if self.can_update(entry):
            self._history.add(entry)

    def can_update(self, entry: SensorEntry) -> bool:
        return self.location == entry.location
