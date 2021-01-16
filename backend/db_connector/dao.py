import sqlalchemy
from sqlalchemy import insert

from db_structure import Wezel
import json
import os


def connection():
    engine = sqlalchemy.engine.create_engine(get_uri())
    return engine.connect()


def get_uri():
    with open(os.path.join(os.path.abspath(__file__), "settings.json")) as file:
        settings = json.load(file)

        return settings['DB_URI']


def get_all_points():
    with connection() as c:
        res = c.execute("select * from wezel")
        print(res)
        return res


def get_all_segment():
    # connect to db
    return ["Morskie Oko - Rysy", "Czarny Staw nad Morskim Okiem - Morskie Oko"]


if __name__ == '__main__':
    with connection() as c:
        ins = insert(Wezel, values={})

