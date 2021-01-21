import sqlalchemy
from sqlalchemy import insert
from backend.db_connector.model.data_models import *
from backend.db_connector.db_structure import *

from collections import defaultdict

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


def insert_route_segments(route_segments, route_id):
    with _connection() as c:
        ins = insert(OdcinekTrasy, values=[{"odcinek_id": segment.segment_id, "trasa_id": route_id,
                                            "punkty_got": segment.score, "kierunek": segment.direction}
                                           for segment in route_segments])
        c.execute(ins)


def get_route_names(tourist_id):
    with _connection() as c:
        result = c.execute("select trasa.id, trasa.nazwa from trasa "
                           f"where trasa.turysta_id = {tourist_id}")

        return {id: name for id, name in result}


def get_full_route(route_id):
    with _connection() as c:
        result = c.execute(f"""select * from trasa
                           full join odcinek_trasy on trasa.id = odcinek_trasy.trasa_id
                           full join odcinek on odcinek_trasy.odcinek_id = odcinek.id
                           full join wezel on odcinek.wezel_id = wezel.id or odcinek.wezel_id2 = wezel.id
                           where trasa.id = {route_id}""")

        route_segments = defaultdict(lambda: {})
        points = {}
        route = {}

        for _, tourist_id, got_id, route_score, status, route_date, route_name, route_segment_id, _, _, _, direction, \
            segment_id, region, point_2, point_1, score, score_reverse, segment_name, distance, \
            height_diff_up, height_diff_down, point_id, point_name, x, y in result:

            route['name'] = route_name
            route['score'] = route_score
            route['status'] = status
            route['tourist_id'] = tourist_id
            route['got_id'] = got_id
            route['date'] = route_date

            if point_id:
                points[point_id] = Point(point_id, point_name, x, y)
                route_segments[route_segment_id]['segment'] = Segment(id=segment_id,
                                                                      name=segment_name,
                                                                      point_1=point_1,
                                                                      point_2=point_2,
                                                                      region=region,
                                                                      score=score,
                                                                      score_reverse=score_reverse,
                                                                      distance=distance,
                                                                      height_diff_up=height_diff_up,
                                                                      height_diff_down=height_diff_down)

                route_segments[route_segment_id]['direction'] = direction

        for route_segment in route_segments.values():
            route_segment['segment'].point_1 = points[route_segment['segment'].point_1]
            route_segment['segment'].point_2 = points[route_segment['segment'].point_2]

        return Route(id=route_id,
                     name=route['name'],
                     tourist_id=route['tourist_id'],
                     got_id=route['got_id'],
                     segments=list(route_segments.values()),
                     score=route['score'],
                     status=route['status'],
                     verification_date=route['date'])


def update_route(route_id, route):
    table = Trasa.__table__
    with _connection() as c:
        ins = table.update().where(table.c.id == route_id).values({"nazwa": route.name, "punkty_got": route.score,
                                                                   "status": route.status})
        c.execute(ins)


def delete_route_segments(route_id):
    with _connection() as c:
        table = OdcinekTrasy.__table__
        delete = table.delete().where(table.c.trasa_id == route_id)

        c.execute(delete)


def delete_route(route_id):
    with _connection() as c:
        table = Trasa.__table__
        delete = table.delete().where(table.c.id == route_id)

        c.execute(delete)


def add_documetnation(route_id, filename):
    with _connection() as c:
        ins = insert(DokumentacjaTrasy, values=[{"trasa_id": route_id, "sciezka": filename}])
        c.execute(ins)


def get_all_documentation(route_id):
    with _connection() as c:
        result = c.execute("select sciezka from dokumentacja_trasy "
                           f"where trasa_id = {route_id}")

    a = [path[0] for path in result]
    return a
