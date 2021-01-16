from backend.db_connector import dao


def get_data_for_browser():
    points = dao.get_all_points()
    segments = dao.get_all_segment()

    return points + segments
