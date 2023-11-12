from . import artist as artist, cbook as cbook
from .artist import Artist as Artist
from .font_manager import FontProperties as FontProperties
from .patches import FancyArrowPatch as FancyArrowPatch, FancyBboxPatch as FancyBboxPatch, Rectangle as Rectangle
from .textpath import TextPath as TextPath, TextToPath as TextToPath
from .transforms import Affine2D as Affine2D, Bbox as Bbox, BboxBase as BboxBase, BboxTransformTo as BboxTransformTo, IdentityTransform as IdentityTransform, Transform as Transform
from _typeshed import Incomplete

class Text(Artist):
    zorder: int
    def __init__(self, x: int = ..., y: int = ..., text: str = ..., *, color: Incomplete | None = ..., verticalalignment: str = ..., horizontalalignment: str = ..., multialignment: Incomplete | None = ..., fontproperties: Incomplete | None = ..., rotation: Incomplete | None = ..., linespacing: Incomplete | None = ..., rotation_mode: Incomplete | None = ..., usetex: Incomplete | None = ..., wrap: bool = ..., transform_rotates_text: bool = ..., parse_math: Incomplete | None = ..., antialiased: Incomplete | None = ..., **kwargs) -> None: ...
    def update(self, kwargs): ...
    def contains(self, mouseevent): ...
    def get_rotation(self): ...
    def get_transform_rotates_text(self): ...
    stale: bool
    def set_rotation_mode(self, m) -> None: ...
    def get_rotation_mode(self): ...
    def set_antialiased(self, antialiased) -> None: ...
    def get_antialiased(self): ...
    def update_from(self, other) -> None: ...
    def set_bbox(self, rectprops) -> None: ...
    def get_bbox_patch(self): ...
    def update_bbox_position_size(self, renderer) -> None: ...
    def set_clip_box(self, clipbox) -> None: ...
    def set_clip_path(self, path, transform: Incomplete | None = ...) -> None: ...
    def set_clip_on(self, b) -> None: ...
    def get_wrap(self): ...
    def set_wrap(self, wrap) -> None: ...
    def draw(self, renderer) -> None: ...
    def get_color(self): ...
    def get_fontproperties(self): ...
    def get_fontfamily(self): ...
    def get_fontname(self): ...
    def get_fontstyle(self): ...
    def get_fontsize(self): ...
    def get_fontvariant(self): ...
    def get_fontweight(self): ...
    def get_stretch(self): ...
    def get_horizontalalignment(self): ...
    def get_unitless_position(self): ...
    def get_position(self): ...
    def get_text(self): ...
    def get_verticalalignment(self): ...
    def get_window_extent(self, renderer: Incomplete | None = ..., dpi: Incomplete | None = ...): ...
    def set_backgroundcolor(self, color) -> None: ...
    def set_color(self, color) -> None: ...
    def set_horizontalalignment(self, align) -> None: ...
    def set_multialignment(self, align) -> None: ...
    def set_linespacing(self, spacing) -> None: ...
    def set_fontfamily(self, fontname) -> None: ...
    def set_fontvariant(self, variant) -> None: ...
    def set_fontstyle(self, fontstyle) -> None: ...
    def set_fontsize(self, fontsize) -> None: ...
    def get_math_fontfamily(self): ...
    def set_math_fontfamily(self, fontfamily) -> None: ...
    def set_fontweight(self, weight) -> None: ...
    def set_fontstretch(self, stretch) -> None: ...
    def set_position(self, xy) -> None: ...
    def set_x(self, x) -> None: ...
    def set_y(self, y) -> None: ...
    def set_rotation(self, s) -> None: ...
    def set_transform_rotates_text(self, t) -> None: ...
    def set_verticalalignment(self, align) -> None: ...
    def set_text(self, s) -> None: ...
    def set_fontproperties(self, fp) -> None: ...
    def set_usetex(self, usetex) -> None: ...
    def get_usetex(self): ...
    def set_parse_math(self, parse_math) -> None: ...
    def get_parse_math(self): ...
    def set_fontname(self, fontname) -> None: ...

class OffsetFrom:
    def __init__(self, artist, ref_coord, unit: str = ...) -> None: ...
    def set_unit(self, unit) -> None: ...
    def get_unit(self): ...
    def __call__(self, renderer): ...

class _AnnotationBase:
    xy: Incomplete
    xycoords: Incomplete
    def __init__(self, xy, xycoords: str = ..., annotation_clip: Incomplete | None = ...) -> None: ...
    def set_annotation_clip(self, b) -> None: ...
    def get_annotation_clip(self): ...
    def draggable(self, state: Incomplete | None = ..., use_blit: bool = ...): ...

class Annotation(Text, _AnnotationBase):
    arrowprops: Incomplete
    arrow_patch: Incomplete
    def __init__(self, text, xy, xytext: Incomplete | None = ..., xycoords: str = ..., textcoords: Incomplete | None = ..., arrowprops: Incomplete | None = ..., annotation_clip: Incomplete | None = ..., **kwargs) -> None: ...
    def contains(self, mouseevent): ...
    @property
    def xycoords(self): ...
    @property
    def xyann(self): ...
    def get_anncoords(self): ...
    def set_anncoords(self, coords) -> None: ...
    anncoords: Incomplete
    def set_figure(self, fig) -> None: ...
    def update_positions(self, renderer): ...
    def draw(self, renderer) -> None: ...
    def get_window_extent(self, renderer: Incomplete | None = ...): ...
    def get_tightbbox(self, renderer: Incomplete | None = ...): ...
