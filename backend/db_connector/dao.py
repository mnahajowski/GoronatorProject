import sqlalchemy
from sqlalchemy import insert
from backend.db_connector.model.data_models import *
from backend.db_connector.db_structure import *

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


def get_points_by_id(points):
    points_parsed = f"({','.join(points)})"
    with _connection() as c:
        result = c.execute(f"select id, nazwa, wspolrzedna_x, wspolrzedna_y from wezel where id in {points_parsed}")

    return [Point(id, name, x, y) for id, name, x, y in result]


def get_segments_by_id(segment_list):
    segments_parsed = f"({','.join(segment_list)})"
    with _connection() as c:
        result = c.execute("select id, region_id, wezel_id2, wezel_id, punkty_got_w_kierunku, "
                           "punkty_got_w_przeciwnym_kierunku, nazwa, odleglosc, suma_podejsc, suma_zejsc from odcinek "
                           f"where id in {segments_parsed}")

    return [Segment(id, name, point_1, point_2, region, score, score_reverse, distance, up, down)
            for id, region, point_2, point_1, score, score_reverse, name, distance, up, down in result]


def get_correlated_segments(point_id):
    with _connection() as c:
        result = c.execute("select id, region_id, wezel_id2, wezel_id, punkty_got_w_kierunku, "
                           "punkty_got_w_przeciwnym_kierunku, nazwa, odleglosc, suma_podejsc, suma_zejsc from odcinek "
                           f"where wezel_id = {point_id} or wezel_id2 = {point_id}")

    return [Segment(id, name, point_1, point_2, region, score, score_reverse, distance, up, down)
            for id, region, point_2, point_1, score, score_reverse, name, distance, up, down in result]


def insert_route(route):
    table = Trasa.__table__
    with _connection() as c:
        ins = table.insert().returning(table.c.id).values([{"nazwa": route.name, "turysta_id": route.tourist_id,
                                                            "punkty_got": route.score, "status": 1}])
        result = c.execute(ins)
        [inserted_id] = result.fetchone()

    return inserted_id


def insert_route_segments(route_segments):
    with _connection() as c:
        ins = insert(OdcinekTrasy, values=[{"odcinek_id": segment.segment_id, "trasa_id": segment.route_id,
                                            "punkty_got": segment.score, "kierunek": segment.direction}
                                           for segment in route_segments])
        c.execute(ins)
