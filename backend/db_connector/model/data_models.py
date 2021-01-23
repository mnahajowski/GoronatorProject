from dataclasses import dataclass
from datetime import datetime

from typing import Union, List


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
    point_1: Union[int, Point]
    point_2: Union[int, Point]
    region: int
    score: int
    score_reverse: int
    distance: int
    height_diff_up: int
    height_diff_down: int


@dataclass
class RouteSegment:
    id: int
    segment_id: Union[int, Segment]
    score: int
    direction: bool


@dataclass
class Route:
    id: int
    name: str
    tourist_id: int
    segments: List[Union[int, RouteSegment]]
    got_id: int
    score: int
    status: int
    verification_date: datetime
