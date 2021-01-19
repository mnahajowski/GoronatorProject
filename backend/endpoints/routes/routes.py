from backend.db_connector.model.data_models import RouteSegment, Route
from backend.db_connector import dao


def insert_new_route(route_raw):
    route = Route(name=route_raw['name'],
                  tourist_id=route_raw['tourist_id'],
                  score=route_raw['score'],
                  id=0,
                  got_id=0,
                  status=0,
                  verification_date=None)

    route_id = dao.insert_route(route)

    segments = [RouteSegment(id=0,
                             segment_id=segment['segment_id'],
                             route_id=route_id,
                             score=segment['score'],
                             direction=segment['direction']) for segment in route_raw['segments']]

    dao.insert_route_segments(segments)

    return route_id
