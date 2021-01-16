import sqlalchemy
from sqlalchemy import insert, select
from backend.db_connector.model.data_models import Point

import json
import os


def _connection():
    engine = sqlalchemy.engine.create_engine(_get_uri())
    return engine.connect()


def _get_uri():
    with open(os.path.join(os.path.dirname(__file__), "settings.json")) as file:
        settings = json.load(file)

        return settings['DB_URI']


def get_points():
    with _connection() as c:
        result = c.execute("select id, nazwa, wspolrzedna_x, wspolrzedna_y from wezel")
        return [Point(id, name, x, y) for id, name, x, y in result]


def get_segment_list():
    with _connection() as c:
        result = c.execute("select id, nazwa from odcinek")
        return [{"id": id, "name": name} for id, name in result]
