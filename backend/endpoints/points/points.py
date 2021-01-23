from backend.db_connector import dao


def get_points():
    return dao.get_points()


def get_segments():
    return dao.get_segments()


def get_points_by_id(points):
    return dao.get_points_by_id(points)


def get_segments_by_ids(segment_list):
    return dao.get_segments_by_id(segment_list)


def get_correlated_segments(point_id):
    return dao.get_correlated_segments(point_id)