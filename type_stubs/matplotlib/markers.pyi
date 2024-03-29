from . import cbook as cbook
from ._enums import CapStyle as CapStyle, JoinStyle as JoinStyle
from .path import Path as Path
from .transforms import Affine2D as Affine2D, IdentityTransform as IdentityTransform
from _typeshed import Incomplete

TICKLEFT: Incomplete
TICKRIGHT: Incomplete
TICKUP: Incomplete
TICKDOWN: Incomplete
CARETLEFT: Incomplete
CARETRIGHT: Incomplete
CARETUP: Incomplete
CARETDOWN: Incomplete
CARETLEFTBASE: Incomplete
CARETRIGHTBASE: Incomplete
CARETUPBASE: Incomplete
CARETDOWNBASE: Incomplete

class MarkerStyle:
    markers: Incomplete
    filled_markers: Incomplete
    fillstyles: Incomplete
    def __init__(self, marker, fillstyle: Incomplete | None = ..., transform: Incomplete | None = ..., capstyle: Incomplete | None = ..., joinstyle: Incomplete | None = ...) -> None: ...
    def __bool__(self) -> bool: ...
    def is_filled(self): ...
    def get_fillstyle(self): ...
    def get_joinstyle(self): ...
    def get_capstyle(self): ...
    def get_marker(self): ...
    def get_path(self): ...
    def get_transform(self): ...
    def get_alt_path(self): ...
    def get_alt_transform(self): ...
    def get_snap_threshold(self): ...
    def get_user_transform(self): ...
    def transformed(self, transform: Affine2D): ...
    def rotated(self, *, deg: Incomplete | None = ..., rad: Incomplete | None = ...): ...
    def scaled(self, sx, sy: Incomplete | None = ...): ...
