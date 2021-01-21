from backend.db_connector.model.data_models import RouteSegment, Route
from backend.db_connector import dao


def insert_new_route(route_raw):
    route = Route(name=route_raw['name'],
                  tourist_id=route_raw['tourist_id'],
                  score=route_raw['score'],
                  segments=[],
                  id=0,
                  got_id=0,
                  status=0,
                  verification_date=route_raw.get('date'))

    route_id = dao.insert_route(route)

    segments = [RouteSegment(id=0,
                             segment_id=segment['segment_id'],
                             score=segment['score'],
                             direction=segment['direction']) for segment in route_raw['segments']]

    dao.insert_route_segments(segments, route_id)

    return route_id


def get_full_route(route_id):
    return dao.get_full_route(route_id)


def get_route_names(tourist_id):
    return dao.get_route_names(tourist_id)


def update_route(route_id, route_raw):
    route = Route(name=route_raw['name'],
                  tourist_id=route_raw['tourist_id'],
                  score=route_raw['score'],
                  segments=[],
                  id=0,
                  got_id=route_raw.get('got_id'),
                  status=route_raw.get('status'),
                  verification_date=route_raw.get('date'))

    dao.delete_route_segments(route_id)

    segments = [RouteSegment(id=0,
                             segment_id=segment['segment_id'],
                             score=segment['score'],
                             direction=segment['direction']) for segment in route_raw['segments']]

    dao.insert_route_segments(segments, route_id)
    dao.update_route(route_id, route)


def delete_route(route_id):
    dao.delete_route_segments(route_id)
    dao.delete_route(route_id)
