from dataclasses import dataclass
from datetime import datetime

from app import db

@dataclass
class Event(db.Model):
    __tablename__ = 'event'
    id: int
    name: str
    location: str
    start_time: datetime
    end_time: datetime
    email: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    location = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DATETIME(), nullable=False)
    end_time = db.Column(db.DATETIME(), nullable=False)
    email = db.Column(db.String, nullable=False)
    delete_flag = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, **kwargs):
        super(Event, self).__init__(**kwargs)

    def __repr__(self):
        return '<Event {}>'.format(self.name)