from backend.db_connector.dao import _connection
from sqlalchemy import insert
from db_structure import *


def insert_data():
    with _connection() as c:
        pass
        # ins = insert(Wezel, values=[{"nazwa": "Rysy", "wspolrzedna_x": 49.17953, "wspolrzedna_y": 20.08806},
        #                             {"nazwa": "Czarny Staw nad Morskim Okiem", "wspolrzedna_x": 49.18827, "wspolrzedna_y": 20.07542},
        #                             {"nazwa": "Schronisko PTTK nad Morskim Okiem", "wspolrzedna_x": 49.201401, "wspolrzedna_y": 20.070999},
        #                             {"nazwa": "Wodogrzmoty Mickiewicza", "wspolrzedna_x": 49.23422, "wspolrzedna_y": 20.08704},
        #                             {"nazwa": "Palenica Białczańskia", "wspolrzedna_x": 49.25501, "wspolrzedna_y": 20.10297}])

        # ins = insert(Odcinek, values=[{"region_id": 1, "wezel_id": 4, "wezel_id2": 3, "nazwa": "Czarny Staw nad Morskim Okiem - Rysy", "punkty_got_w_kierunku": 13, "punkty_got_w_przeciwnym_kierunku": 4},
        #                               {"region_id": 1, "wezel_id": 5, "wezel_id2": 4, "nazwa": "Schronisko PTTK nad Morskim Okiem - Czarny Staw nad Morskim Okiem", "punkty_got_w_kierunku": 4, "punkty_got_w_przeciwnym_kierunku": 2},
        #                               {"region_id": 1, "wezel_id": 5, "wezel_id2": 6, "nazwa": "Schronisko PTTK nad Morskim Okiem - Wodogrzmoty Mickiewicza", "punkty_got_w_kierunku": 5, "punkty_got_w_przeciwnym_kierunku": 8},
        #                               {"region_id": 1, "wezel_id": 6, "wezel_id2": 7, "nazwa": "Wodogrzmoty Mickiewicza - Palenica Białczańskia", "punkty_got_w_kierunku": 3, "punkty_got_w_przeciwnym_kierunku": 4}])
        #
        # c.execute(ins)


if __name__ == '__main__':
    insert_data()
