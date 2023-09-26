from datetime import datetime

from sqlalchemy import text

from weatherapp.domain import model


def test_sensorentry_mapper_can_load_lines(session):
    session.execute(
        text(
            "INSERT INTO sensor_entries (temperature, humidity, wind_speed, location, date_and_time) VALUES"
            '(25, 44, 55, "Cork", "2011-04-11"),'
            '(25, 44, 57, "Cork", "2011-04-12")'
        )
    )
    expected = [
        model.SensorEntry(25.0, 44.0, 55.0, "Cork", datetime(2011, 4, 11)),
        model.SensorEntry(25.0, 44.0, 57.0, "Cork", datetime(2011, 4, 12)),
    ]
    assert session.query(model.SensorEntry).all() == expected


def test_saving_updates(session):
    weather_history = model.WeatherHistory("Sesnor1", "Cork")
    entry = model.SensorEntry(25.0, 44.0, 55.0, "Cork", datetime(2011, 4, 11))
    weather_history.update(entry)
    session.add(weather_history)
    session.commit()

    rows = list(session.execute(text("SELECT weatherhistory_id, sensorentry_id FROM history")))
    assert rows == [(weather_history.id, entry.id)]
