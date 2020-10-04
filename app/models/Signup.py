from dataclasses import dataclass

from sqlalchemy import UniqueConstraint

from app import db


@dataclass
class Signup(db.Model):
    __tablename__ = 'signup'
    id: int
    user_id: int
    event_id: int
    user_email: str
    event_name: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user = db.relationship('User', foreign_keys=user_id, uselist=False)
    event = db.relationship('Event', foreign_keys=event_id, uselist=False)
    user_email = ""
    event_name = ""

    __table_args__ = (UniqueConstraint('user_id', 'event_id', name='_user_event_uc'),
                      )

    def __init__(self, **kwargs):
        super(Signup, self).__init__(**kwargs)

    def __repr__(self):
        return '<Signup {}>'.format(self.user_id + ":" + self.event_id)

    def setInfo(self):
        self.user_email = self.user.email
        self.event_name = self.event.name