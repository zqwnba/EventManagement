# Event Management Application

Demo application based on Flask

## Installation

First, you need to clone this repo:

```bash
$ git clone https://github.com/zqwnba/EventManagement.git
```

Then change into the `EventManagement` folder, create a virtual environment and install all the dependencies.

Use pip + virtualenv:

```bash
$ cd EventManagement
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## How to Run This Application?

**Before run, we can initialize the SQLite database:**

```bash
$ python app/initdb/db.py

Initialized the database.
close the connection.
```
Initial DB schema and data can be found and edited in ```app/initdb/schema.sql``` and ```app/initdb/init_data.sql```

Then, start the celery task to send notification/invitation email asynchronously 
```bash
$ celery -A app.celery_app worker -l INFO
```

Then (in separated terminal) start the service locally

```bash
$ export FLASK_APP=app
$ export FLASK_ENV=development
$ flask run
```
The applications will be running on http://localhost:5000 by default. 
Use ```flask run -h {HOST} -p {PORT}``` to customize HOST and PORT

NOTE: If got error like **```ModuleNotFoundError: No module named 'flask_restplus'```**, please re-entry the virtual env.
```bash
$ deactivate
$ source venv/bin/activate
```

## Endpoints

- Swagger UI (`/api/v1`): Shows API specification. Try here: http://localhost:5000/api/v1
- User (`/users`): User management
- Event (`/events`): User management
- Sign-up (`/signups`): Reservation management

## Example Request and Response
### Event Management
* Show pre-defined events
```bash
$ curl --request GET 'http://127.0.0.1:5000/api/v1/events'

[
    {
        "id": 0,
        "name": "FUJI ROCK FESTIVAL '20",
        "location": "Naeba Ski Resort, Yuzawa-cho, Niigata Pref.",
        "start_time": "2020-08-21T10:00:00",
        "end_time": "2020-08-23T17:00:00",
        "email": "contact@fujirockfestival.com"
    },
    ...
]
```

* Creat a new event
```bash
$ curl --request POST 'http://127.0.0.1:5000/api/v1/events' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "email": "contact@fujirockfestival.com",
    "end_time": "2021-08-23T17:00:00",
    "location": "Naeba Ski Resort, Yuzawa-cho, Niigata Pref.",
    "name": "FUJI ROCK FESTIVAL '\''21",
    "start_time": "2021-08-21T10:00:00"
  }'

{
    "id": 5,
    "name": "FUJI ROCK FESTIVAL '21",
    "location": "Naeba Ski Resort, Yuzawa-cho, Niigata Pref.",
    "start_time": "2021-08-21T10:00:00",
    "end_time": "2021-08-23T17:00:00",
    "email": "contact@fujirockfestival.com"
}
```

* Delete pre-defined event
```bash
$ curl --request DELETE 'http://127.0.0.1:5000/api/v1/events/5'

[
    {
        "id": 5,
        "name": "FUJI ROCK FESTIVAL '21",
        "location": "Naeba Ski Resort, Yuzawa-cho, Niigata Pref.",
        "start_time": "2021-08-21T10:00:00",
        "end_time": "2021-08-23T17:00:00",
        "email": "contact@fujirockfestival.com"
    }
]
```
### User Management
**A user has to register to the system before signing up to an event**

* Register a new users
```bash
$ curl --request POST 'http://127.0.0.1:5000/api/v1/users' \
  --header 'Content-Type: application/json' \
  --data-raw '{
      "email":"user3@gmail.com"
  }'
```

* Show registered users
```bash
$ curl --request GET 'http://127.0.0.1:5000/api/v1/users'
[
    {
        "id": 0,
        "email": "user1@gmail.com"
    },
    {
        "id": 1,
        "email": "user2@gmail.com"
    },
    {
        "id": 2,
        "email": "user3@gmail.com"
    }
]
```

### Sign-up and Sign-out
* Sign up for a event

**A user has to register to the system before signing up to an event**
```bash
$ curl --request POST 'http://127.0.0.1:5000/api/v1/signups' \
  --header 'Content-Type: application/json' \
  --data-raw '{
      "event_name": "FUJI ROCK FESTIVAL '\''17",
      "user_email": "user2@gmail.com"
  }'

{
    "id": 1,
    "user_id": 1,
    "event_id": 3,
    "user_email": "user2@gmail.com",
    "event_name": "FUJI ROCK FESTIVAL '17"
}
```
```ConnectionRefusedError: [Errno 61] Connection refused``` would be shown on celery task when application tries to notification/invitation email asynchronously.
Because the mail setting uses dummy data. Please change the email setting in ```app/__init__.py```.

* Sign out for a event
```bash
$ curl --request DELETE 'http://127.0.0.1:5000/api/v1/signups' \
  --header 'Content-Type: application/json' \
  --data-raw '{
      "event_name": "FUJI ROCK FESTIVAL '\''17",
      "user_email": "user2@gmail.com"
  }'

{
    "id": 1,
    "user_id": 1,
    "event_id": 3,
    "user_email": "user2@gmail.com",
    "event_name": "FUJI ROCK FESTIVAL '17"
}
```

