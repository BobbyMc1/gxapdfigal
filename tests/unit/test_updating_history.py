from datetime import datetime

from weatherapp.domain.model import SensorEntry, WeatherHistory


def test_updating_is_idempotent():
    history = WeatherHistory("Today", "Cork")
    entry = SensorEntry(15, 23, 35, "Cork", datetime.now())

    history.update(entry)
    history.update(entry)

    assert len(history._history) == 1
