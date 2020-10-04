import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    print("get_db")
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = sqlite3.connect("instance/test.db")
    return db


def init_db():
    db = get_db()
    print("write to db")
    with current_app.open_resource('db/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    with current_app.open_resource('db/init_data.sql') as f:
        db.executescript(f.read().decode('utf8'))
    #print("write to db")


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
    print("start to init db")
    app.cli.add_command(init_db_command())
    print("end to init db")