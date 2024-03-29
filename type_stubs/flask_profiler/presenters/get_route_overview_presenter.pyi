from flask_profiler.use_cases import get_route_overview as use_case
from typing import Iterable, List, Optional

class Plot:
    data_points: list[Point]
    x_axis: Line
    y_axis: Line
    x_markings: list[Line]
    y_markings: list[Line]
    @property
    def point_connections(self) -> Iterable[Line]: ...
    def transform(self, transformation: Conversion) -> Plot: ...
    def __init__(self, data_points, x_axis, y_axis, x_markings, y_markings) -> None: ...

class Point:
    @property
    def x(self) -> str: ...
    @property
    def y(self) -> str: ...
    def __init__(self, _x, _y) -> None: ...

class Line:
    p1: Point
    p2: Point
    label: Optional[str]
    @property
    def x1(self) -> str: ...
    @property
    def y1(self) -> str: ...
    @property
    def x2(self) -> str: ...
    @property
    def y2(self) -> str: ...
    def __init__(self, p1, p2, label) -> None: ...

class Graph:
    title: str
    width: str
    height: str
    plot: Plot
    def __init__(self, title, width, height, plot) -> None: ...

class ViewModel:
    headline: str
    graphs: List[Graph]
    def __init__(self, headline, graphs) -> None: ...

class GetRouteOverviewPresenter:
    def present_response(self, response: use_case.Response) -> ViewModel: ...

class Conversion:
    rows: List[List[float]]
    @classmethod
    def stretch(cls, *, x: float = ..., y: float = ...) -> Conversion: ...
    @classmethod
    def translation(cls, *, x: float = ..., y: float = ...) -> Conversion: ...
    @classmethod
    def mirror_y(cls) -> Conversion: ...
    def transform_point(self, p: Point) -> Point: ...
    def transform_line(self, line: Line) -> Line: ...
    def concat(self, other: Conversion) -> Conversion: ...
    def __getitem__(self, x: int) -> List[float]: ...
    def __init__(self, rows) -> None: ...
