from dataclasses import dataclass

from app.extensions import db

@dataclass
class User(db.Model):
    __tablename__ = 'user'
    id: int
    email: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    delete_flag = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '<User {}>'.format(self.email)