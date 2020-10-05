import os
import sqlite3

from flask import g, Flask

app = Flask(__name__)


def get_db():
    if 'db' not in g:
        # ensure the instance folder exists
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

        g.db = sqlite3.connect(
            os.path.join(app.instance_path, 'app.sqlite'),
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def init_db():
    db = get_db()
    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    with app.open_resource('init_data.sql') as f:
        db.executescript(f.read().decode('utf8'))


def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    print('Initialized the database.')
    close_db()


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        print('close the connection.')
        db.close()


if __name__ == '__main__':
    with app.app_context():
        init_db_command()