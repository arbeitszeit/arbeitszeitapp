from _typeshed import Incomplete
from matplotlib import backend_bases as backend_bases, backend_tools as backend_tools
from matplotlib.backend_bases import KeyEvent as KeyEvent, LocationEvent as LocationEvent, MouseEvent as MouseEvent, ResizeEvent as ResizeEvent, _Backend
from matplotlib.backends import backend_agg as backend_agg

class TimerTornado(backend_bases.TimerBase):
    def __init__(self, *args, **kwargs) -> None: ...

class TimerAsyncio(backend_bases.TimerBase):
    def __init__(self, *args, **kwargs) -> None: ...

class FigureCanvasWebAggCore(backend_agg.FigureCanvasAgg):
    manager_class: Incomplete
    supports_blit: bool
    def __init__(self, *args, **kwargs) -> None: ...
    def show(self) -> None: ...
    def draw(self) -> None: ...
    def blit(self, bbox: Incomplete | None = ...) -> None: ...
    def draw_idle(self) -> None: ...
    def set_cursor(self, cursor) -> None: ...
    def set_image_mode(self, mode) -> None: ...
    def get_diff_image(self): ...
    def handle_event(self, event): ...
    def handle_unknown_event(self, event) -> None: ...
    def handle_ack(self, event) -> None: ...
    def handle_draw(self, event) -> None: ...
    handle_button_press: Incomplete
    handle_button_release: Incomplete
    handle_dblclick: Incomplete
    handle_figure_enter: Incomplete
    handle_figure_leave: Incomplete
    handle_motion_notify: Incomplete
    handle_scroll: Incomplete
    handle_key_press: Incomplete
    handle_key_release: Incomplete
    def handle_toolbar_button(self, event) -> None: ...
    def handle_refresh(self, event) -> None: ...
    def handle_resize(self, event) -> None: ...
    def handle_send_image_mode(self, event) -> None: ...
    def handle_set_device_pixel_ratio(self, event) -> None: ...
    def handle_set_dpi_ratio(self, event) -> None: ...
    def send_event(self, event_type, **kwargs) -> None: ...

class NavigationToolbar2WebAgg(backend_bases.NavigationToolbar2):
    toolitems: Incomplete
    message: str
    def __init__(self, canvas) -> None: ...
    def set_message(self, message) -> None: ...
    def draw_rubberband(self, event, x0, y0, x1, y1) -> None: ...
    def remove_rubberband(self) -> None: ...
    def save_figure(self, *args) -> None: ...
    def pan(self) -> None: ...
    def zoom(self) -> None: ...
    def set_history_buttons(self) -> None: ...

class FigureManagerWebAgg(backend_bases.FigureManagerBase):
    ToolbarCls = NavigationToolbar2WebAgg
    web_sockets: Incomplete
    def __init__(self, canvas, num) -> None: ...
    def show(self) -> None: ...
    def resize(self, w, h, forward: bool = ...) -> None: ...
    def set_window_title(self, title) -> None: ...
    def get_window_title(self): ...
    def add_web_socket(self, web_socket) -> None: ...
    def remove_web_socket(self, web_socket) -> None: ...
    def handle_json(self, content) -> None: ...
    def refresh_all(self) -> None: ...
    @classmethod
    def get_javascript(cls, stream: Incomplete | None = ...): ...
    @classmethod
    def get_static_file_path(cls): ...

class _BackendWebAggCoreAgg(_Backend):
    FigureCanvas = FigureCanvasWebAggCore
    FigureManager = FigureManagerWebAgg
