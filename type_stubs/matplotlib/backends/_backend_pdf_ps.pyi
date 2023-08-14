from .. import font_manager as font_manager, ft2font as ft2font
from .._afm import AFM as AFM
from ..backend_bases import RendererBase as RendererBase
from _typeshed import Incomplete

def get_glyphs_subset(fontfile, characters): ...

class CharacterTracker:
    used: Incomplete
    def __init__(self) -> None: ...
    def track(self, font, s) -> None: ...
    def track_glyph(self, font, glyph) -> None: ...

class RendererPDFPSBase(RendererBase):
    width: Incomplete
    height: Incomplete
    def __init__(self, width, height) -> None: ...
    def flipy(self): ...
    def option_scale_image(self): ...
    def option_image_nocomposite(self): ...
    def get_canvas_width_height(self): ...
    def get_text_width_height_descent(self, s, prop, ismath): ...