from dataclasses import dataclass


@dataclass
class Point:
    id: int
    name: str
    x: float
    y: float


@dataclass
class Segment:
    id: int
    name: str
    point_1: int
    point_2: int
    region: int
    score: int
    score_reverse: int
    distance: int
    height_diff_up: int
    height_diff_down: int
