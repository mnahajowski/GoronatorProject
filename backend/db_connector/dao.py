import sqlalchemy
from sqlalchemy import insert, select
from backend.db_connector.model.data_models import *

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


def get_segments():
    with _connection() as c:
        result = c.execute("select id, region_id, wezel_id2, wezel_id, punkty_got_w_kierunku, "
                           "punkty_got_w_przeciwnym_kierunku, nazwa, odleglosc, suma_podejsc, suma_zejsc from odcinek")
    return [Segment(id, name, point_1, point_2, region, score, score_reverse, distance, up, down)
            for id, region, point_2, point_1, score, score_reverse, name, distance, up, down in result]
