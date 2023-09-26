import json
import random

import requests
from faker import Faker


def post_sensor_entry(temp, hum, wind, date):
    url = "http://localhost:8000/sensor-entries"

    body = {"temperature": temp, "humidity": hum, "wind_speed": wind, "location": "Cork", "date_and_time": date}
    body
    try:
        req = requests.post(url=url, data=json.dumps(body, default=str))
        print(req.status_code)

    except Exception as e:
        print(e)


def post_weather_history_entry():
    url = "http://localhost:8000/location"

    body = {"reference": "Sensor1", "location": "Cork"}
    body
    try:
        req = requests.post(url=url, data=json.dumps(body, default=str))
        print(req.status_code)

    except Exception as e:
        print(e)


def get_weather_sensor_data():
    url = "http://localhost:8000/locations"
    try:
        req = requests.get(url=url, params={"location": "Cork", "statistic": "min"})
        print(req.status_code, req.text)

    except Exception as e:
        print(e)


def test_happy_path_uploading_sensor_data():
    fake = Faker()
    url = "http://localhost:8000/sensor-entries"
    body = {
        "temperature": random.uniform(0, 100),
        "humidity": random.uniform(0, 100),
        "wind_speed": random.uniform(0, 100),
        "location": "Cork",
        "date_and_time": fake.date_time_between(start_date="-30d", end_date="now"),
    }

    req = requests.post(url=url, data=json.dumps(body, default=str))

    assert req.status_code == 201


def test_happy_path_for_querying_sensor_data_with_start_and_end_date():
    url = "http://localhost:8000/sensor-data"
    req = requests.get(
        url=url,
        params={
            "location": "Cork",
            "statistic": "min",
            "start_date": "2023-08-12T00:00:00",
            "end_date": "2023-09-12T00:00:00",
        },
    )

    assert req.status_code == 200


def test_happy_path_for_querying_sensor_data_with__no_start_and_end_date():
    url = "http://localhost:8000/sensor-data"
    req = requests.get(
        url=url,
        params={
            "location": "Cork",
            "statistic": "min",
        },
    )

    assert req.status_code == 200
