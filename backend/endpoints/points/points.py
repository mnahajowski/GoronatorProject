from backend.db_connector import dao


def get_data_for_browser():
    points = dao.get_points()
    segments = dao.get_segment_list()

    return points + segments
