# WeatherAPP


## Tech Stack
 - Python
 - FastAPI
 - SQLAlchemy
 - SQLite
 - Pytest

## Running APP
- Python version required >=3.10.7
- install a virtual env on local machine.
```python
python -m venv venv
```
- Install requirements.txt with pip.
- To run the weather api, run the following command inside your venv, at the workspace directory level:

```
uvicorn weatherapp.entrypoints.fastapi_app:app
```
- The api will be running at http://127.0.0.1:8000/ and the api docs will be located at http://127.0.0.1:8000/docs#/.

## Approach

### Overview
- The design approach for the api is that our domain, which in this case is the sensor data, should not depend on low level modules such as infrastructure. Quite common in industry to follow this practice, mostly referred to as onion architecture.

- I utilized an ORM as it provides us with that fact our domain can be clean of database dependencies.

- I also utilized the repo pattern and a service layer within the api.

- Note in the current structure, there is still quite a lot of communication across the layers, can see this in the entrypoint of the api, and as always there is room for improvement.

### Domain Overview

- I defined the domain as follows, the sensor entry is what gets recorded from a sensor, Our sensor records wind speed, temperature, humidity, its location and time it was recorded. Our weather history is identified by its location and sensor it came from (reference). Our weather history is made of multiple sensor entries.

- If a sensor entry can't find a corresponding location in the history, it won't be accepted.


### Technologies
- I decided to use FastAPI as the framework as It is something I had been meaning to investigate for awhile now. I found it quite good. I wont't list out all the reasons one would choose this, its well documented on there website, but being able to use pydantic validation for the endpoints and auto generating of docs using OpenAPI spec were really nice features.


## How to interact with the API
- Please refer to the test_api.py module in the E2E test package to view how to .
- You can generate API calls through the automatic docs generated, which are located at http://127.0.0.1:8000/docs#/. There is a try it out button, which will allow you to execute the specific call through the UI.
- Only sensor data can be uploaded for the Cork location, as this is the only weather history location within the DB currently. Another location can be added through the /location endpoint. Please use Cork as the location parameter for the call to get sensor data.
- Note: for the date_and_time param for uploading sensor entries, please use isoformatted time such as '2023-09-12T00:00:00.00' and use location as Cork, as explained above.
- The DB currently has approx 150  sensor entries, and recording started on the start date of 2023-08-16T00:00:00.

## App Requirements Achieved 
- The app can receive new sensor entries at the /sensor-data endpoint
- The data is persisted through using an sqlite db which is part of the repo.
- Input validation is handled by FastAPI.
- The app allows querying of sensor data.
    -  The data returned includes the following data: Temperature, Wind Speed, Humidity, location, and name of Sensor.
    - The min, max, or average of the numeric weather values are returned, depending on which statistic is chosen as the parameter for the query.
    - Allows specifying a start and end range. Where no range us given, the value of data over the last 30 days is returned.





