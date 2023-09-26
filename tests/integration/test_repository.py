from datetime import datetime

from sqlalchemy import text

from weatherapp.adapters.repository import SqlAlchemyRepository
from weatherapp.domain.model import SensorEntry, WeatherHistory


def insert_sensor_entry(session):
    session.execute(
        text(
            """INSERT INTO sensor_entries (temperature, humidity, wind_speed, location, date_and_time) VALUES
            (:temperature, :humidity, :wind_speed, :location, :date_and_time)""",
        ),
        dict(temperature=25, humidity=44, wind_speed=55, location="Cork", date_and_time=datetime(2011, 4, 11)),
    )
    sql_2 = text("SELECT id FROM sensor_entries WHERE location=:location AND date_and_time=:date_and_time")
    [[sensorentry_id]] = session.execute(sql_2, dict(location="Cork", date_and_time=datetime(2011, 4, 11)))

    return sensorentry_id


def insert_weather_history(session, sensor_id):
    insert_statement = text("INSERT INTO weather_history (reference, location) VALUES (:reference, :location)")
    session.execute(insert_statement, dict(reference=sensor_id, location="Cork"))

    select_statement = text("SELECT id FROM weather_history WHERE reference=:reference")
    [[weatherhistory_id]] = session.execute(select_statement, dict(reference=sensor_id))

    return weatherhistory_id


def insert_history(session, sensorentry_id, weatherhistory_id):
    insert_statement = text(
        "INSERT INTO history (sensorentry_id, weatherhistory_id) VALUES (:sensorentry_id, :weatherhistory_id)"
    )
    session.execute(
        insert_statement,
        dict(sensorentry_id=sensorentry_id, weatherhistory_id=weatherhistory_id),
    )


def test_repository_can_save_weather_history(session):
    weather_history = WeatherHistory("today", "Cork")

    repo = SqlAlchemyRepository(session)
    repo.add(weather_history)
    session.commit()

    rows = session.execute(text("SELECT reference, location FROM weather_history"))

    assert list(rows) == [("today", "Cork")]


def test_repository_can_retrieve_a_weather_history_with_history(session):
    sensorentry_id = insert_sensor_entry(session)
    weatherhistory_id = insert_weather_history(session, "Reading1")
    insert_weather_history(session, "Reading2")
    insert_history(session, sensorentry_id, weatherhistory_id)

    repo = SqlAlchemyRepository(session)
    retrieved = repo.get("Reading1")

    expected = WeatherHistory("Reading1", "Cork")
    assert retrieved.reference == expected.reference
    assert retrieved.location == expected.location
    assert retrieved._history == {
        SensorEntry(25.0, 44.0, 55.0, "Cork", datetime(2011, 4, 11)),
    }
