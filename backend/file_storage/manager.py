import time
import os


BASE_PATH = os.path.join(os.path.dirname(__file__), 'data')


def get_storage(filename, tourist, route):
    filename = f"{str(time.time()).replace('.', '_')}_{filename}"[-255:]
    full_path = os.path.join(BASE_PATH, tourist, route, filename)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    return filename, full_path


def get_documentation(tourist, route, image):
    return os.path.join(BASE_PATH, tourist, route, image)
