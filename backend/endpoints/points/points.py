from backend.db_connector import dao


def get_points():
    return dao.get_points()


def get_segments():
    return dao.get_segments()
