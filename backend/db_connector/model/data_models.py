from dataclasses import dataclass
from datetime import datetime


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


@dataclass
class Route:
    id: int
    name: str
    tourist_id: int
    got_id: int
    score: int
    status: int
    verification_date: datetime


@dataclass
class RouteSegment:
    id: int
    segment_id: int
    route_id: int
    score: int
    direction: bool
