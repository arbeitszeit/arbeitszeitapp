import PIL.Image
import datetime
import matplotlib.image
import numpy as np
import os
import pathlib
from .ticker import AutoLocator as AutoLocator, FixedFormatter as FixedFormatter, FixedLocator as FixedLocator, FormatStrFormatter as FormatStrFormatter, Formatter as Formatter, FuncFormatter as FuncFormatter, IndexLocator as IndexLocator, LinearLocator as LinearLocator, Locator as Locator, LogFormatter as LogFormatter, LogFormatterExponent as LogFormatterExponent, LogFormatterMathtext as LogFormatterMathtext, LogLocator as LogLocator, MaxNLocator as MaxNLocator, MultipleLocator as MultipleLocator, NullFormatter as NullFormatter, NullLocator as NullLocator, ScalarFormatter as ScalarFormatter, TickHelper as TickHelper
from _typeshed import Incomplete
from collections.abc import Callable as Callable, Hashable, Iterable, Sequence
from contextlib import AbstractContextManager, ExitStack
from cycler import cycler as cycler
from matplotlib import cbook as cbook, interactive as interactive, mlab as mlab, rcParamsDefault as rcParamsDefault, rcParamsOrig as rcParamsOrig, rcsetup as rcsetup
from matplotlib.artist import Artist as Artist
from matplotlib.axes import Axes as Axes, Subplot as Subplot
from matplotlib.axes._base import _AxesBase
from matplotlib.axis import Tick as Tick
from matplotlib.backend_bases import Event as Event, FigureCanvasBase as FigureCanvasBase, FigureManagerBase as FigureManagerBase, MouseButton as MouseButton, RendererBase as RendererBase
from matplotlib.cm import ScalarMappable as ScalarMappable, register_cmap as register_cmap
from matplotlib.collections import BrokenBarHCollection as BrokenBarHCollection, Collection as Collection, EventCollection as EventCollection, LineCollection as LineCollection, PathCollection as PathCollection, PolyCollection as PolyCollection, QuadMesh as QuadMesh
from matplotlib.colorbar import Colorbar as Colorbar
from matplotlib.colors import Colormap as Colormap, Normalize as Normalize
from matplotlib.container import BarContainer as BarContainer, ErrorbarContainer as ErrorbarContainer, StemContainer as StemContainer
from matplotlib.contour import ContourSet as ContourSet, QuadContourSet as QuadContourSet
from matplotlib.figure import Figure as Figure, FigureBase as FigureBase, SubFigure as SubFigure, figaspect as figaspect
from matplotlib.gridspec import GridSpec as GridSpec, SubplotSpec as SubplotSpec
from matplotlib.image import AxesImage as AxesImage, FigureImage as FigureImage
from matplotlib.legend import Legend as Legend
from matplotlib.lines import Line2D as Line2D
from matplotlib.mlab import GaussianKDE as GaussianKDE
from matplotlib.patches import Arrow as Arrow, Circle as Circle, FancyArrow as FancyArrow, Polygon as Polygon, Rectangle as Rectangle, StepPatch as StepPatch, Wedge as Wedge
from matplotlib.projections import PolarAxes as PolarAxes
from matplotlib.quiver import Barbs as Barbs, Quiver as Quiver, QuiverKey as QuiverKey
from matplotlib.scale import ScaleBase as ScaleBase, get_scale_names as get_scale_names
from matplotlib.text import Annotation as Annotation, Text as Text
from matplotlib.transforms import Bbox as Bbox, Transform as Transform
from matplotlib.typing import ColorType as ColorType, HashableList as HashableList, LineStyleType as LineStyleType, MarkerType as MarkerType
from matplotlib.widgets import Button as Button, Slider as Slider, SubplotTool as SubplotTool, Widget as Widget
from numpy.typing import ArrayLike as ArrayLike
from typing import Any, BinaryIO, Literal, overload

colormaps: Incomplete
color_sequences: Incomplete

def install_repl_displayhook() -> None: ...
def uninstall_repl_displayhook() -> None: ...

draw_all: Incomplete

def set_loglevel(*args, **kwargs) -> None: ...
def findobj(o: Artist | None = ..., match: Callable[[Artist], bool] | type[Artist] | None = ..., include_self: bool = ...) -> list[Artist]: ...
def switch_backend(newbackend: str) -> None: ...
def new_figure_manager(*args, **kwargs): ...
def draw_if_interactive(*args, **kwargs): ...
def show(*args, **kwargs) -> None: ...
def isinteractive() -> bool: ...
def ioff() -> ExitStack: ...
def ion() -> ExitStack: ...
def pause(interval: float) -> None: ...
def rc(group: str, **kwargs) -> None: ...
def rc_context(rc: dict[str, Any] | None = ..., fname: str | pathlib.Path | os.PathLike | None = ...) -> AbstractContextManager[None]: ...
def rcdefaults() -> None: ...
def getp(obj, *args, **kwargs): ...
def get(obj, *args, **kwargs): ...
def setp(obj, *args, **kwargs): ...
def xkcd(scale: float = ..., length: float = ..., randomness: float = ...) -> ExitStack: ...
def figure(num: int | str | Figure | SubFigure | None = ..., figsize: tuple[float, float] | None = ..., dpi: float | None = ..., *, facecolor: ColorType | None = ..., edgecolor: ColorType | None = ..., frameon: bool = ..., FigureClass: type[Figure] = ..., clear: bool = ..., **kwargs) -> Figure: ...
def gcf() -> Figure: ...
def fignum_exists(num: int) -> bool: ...
def get_fignums() -> list[int]: ...
def get_figlabels() -> list[Any]: ...
def get_current_fig_manager() -> FigureManagerBase | None: ...
def connect(s: str, func: Callable[[Event], Any]) -> int: ...
def disconnect(cid: int) -> None: ...
def close(fig: None | int | str | Figure | Literal['all'] = ...) -> None: ...
def clf() -> None: ...
def draw() -> None: ...
def savefig(*args, **kwargs) -> None: ...
def figlegend(*args, **kwargs) -> Legend: ...
def axes(arg: None | tuple[float, float, float, float] = ..., **kwargs) -> matplotlib.axes.Axes: ...
def delaxes(ax: matplotlib.axes.Axes | None = ...) -> None: ...
def sca(ax: Axes) -> None: ...
def cla() -> None: ...
def subplot(*args, **kwargs) -> Axes: ...
def subplots(nrows: int = ..., ncols: int = ..., *, sharex: bool | Literal['none', 'all', 'row', 'col'] = ..., sharey: bool | Literal['none', 'all', 'row', 'col'] = ..., squeeze: bool = ..., width_ratios: Sequence[float] | None = ..., height_ratios: Sequence[float] | None = ..., subplot_kw: dict[str, Any] | None = ..., gridspec_kw: dict[str, Any] | None = ..., **fig_kw) -> tuple[Figure, Any]: ...
@overload
def subplot_mosaic(mosaic: str, *, sharex: bool = ..., sharey: bool = ..., width_ratios: ArrayLike | None = ..., height_ratios: ArrayLike | None = ..., empty_sentinel: str = ..., subplot_kw: dict[str, Any] | None = ..., gridspec_kw: dict[str, Any] | None = ..., per_subplot_kw: dict[str | tuple[str, ...], dict[str, Any]] | None = ..., **fig_kw: Any) -> tuple[Figure, dict[str, matplotlib.axes.Axes]]: ...
@overload
def subplot_mosaic(mosaic: list[HashableList[_T]], *, sharex: bool = ..., sharey: bool = ..., width_ratios: ArrayLike | None = ..., height_ratios: ArrayLike | None = ..., empty_sentinel: _T = ..., subplot_kw: dict[str, Any] | None = ..., gridspec_kw: dict[str, Any] | None = ..., per_subplot_kw: dict[_T | tuple[_T, ...], dict[str, Any]] | None = ..., **fig_kw: Any) -> tuple[Figure, dict[_T, matplotlib.axes.Axes]]: ...
@overload
def subplot_mosaic(mosaic: list[HashableList[Hashable]], *, sharex: bool = ..., sharey: bool = ..., width_ratios: ArrayLike | None = ..., height_ratios: ArrayLike | None = ..., empty_sentinel: Any = ..., subplot_kw: dict[str, Any] | None = ..., gridspec_kw: dict[str, Any] | None = ..., per_subplot_kw: dict[Hashable | tuple[Hashable, ...], dict[str, Any]] | None = ..., **fig_kw: Any) -> tuple[Figure, dict[Hashable, matplotlib.axes.Axes]]: ...
def subplot2grid(shape: tuple[int, int], loc: tuple[int, int], rowspan: int = ..., colspan: int = ..., fig: Figure | None = ..., **kwargs) -> matplotlib.axes.Axes: ...
def twinx(ax: matplotlib.axes.Axes | None = ...) -> _AxesBase: ...
def twiny(ax: matplotlib.axes.Axes | None = ...) -> _AxesBase: ...
def subplot_tool(targetfig: Figure | None = ...) -> SubplotTool | None: ...
def box(on: bool | None = ...) -> None: ...
def xlim(*args, **kwargs) -> tuple[float, float]: ...
def ylim(*args, **kwargs) -> tuple[float, float]: ...
def xticks(ticks: ArrayLike | None = ..., labels: Sequence[str] | None = ..., *, minor: bool = ..., **kwargs) -> tuple[list[Tick] | np.ndarray, list[Text]]: ...
def yticks(ticks: ArrayLike | None = ..., labels: Sequence[str] | None = ..., *, minor: bool = ..., **kwargs) -> tuple[list[Tick] | np.ndarray, list[Text]]: ...
def rgrids(radii: ArrayLike | None = ..., labels: Sequence[str | Text] | None = ..., angle: float | None = ..., fmt: str | None = ..., **kwargs) -> tuple[list[Line2D], list[Text]]: ...
def thetagrids(angles: ArrayLike | None = ..., labels: Sequence[str | Text] | None = ..., fmt: str | None = ..., **kwargs) -> tuple[list[Line2D], list[Text]]: ...
def get_plot_commands() -> list[str]: ...
def colorbar(mappable: ScalarMappable | None = ..., cax: matplotlib.axes.Axes | None = ..., ax: matplotlib.axes.Axes | Iterable[matplotlib.axes.Axes] | None = ..., **kwargs) -> Colorbar: ...
def clim(vmin: float | None = ..., vmax: float | None = ...) -> None: ...
def get_cmap(name: Colormap | str | None = ..., lut: int | None = ...) -> Colormap: ...
def set_cmap(cmap: Colormap | str) -> None: ...
def imread(fname: str | pathlib.Path | BinaryIO, format: str | None = ...) -> np.ndarray: ...
def imsave(fname: str | os.PathLike | BinaryIO, arr: ArrayLike, **kwargs) -> None: ...
def matshow(A: ArrayLike, fignum: None | int = ..., **kwargs) -> AxesImage: ...
def polar(*args, **kwargs) -> list[Line2D]: ...
def figimage(X: ArrayLike, xo: int = ..., yo: int = ..., alpha: float | None = ..., norm: str | Normalize | None = ..., cmap: str | Colormap | None = ..., vmin: float | None = ..., vmax: float | None = ..., origin: Literal['upper', 'lower'] | None = ..., resize: bool = ..., **kwargs) -> FigureImage: ...
def figtext(x: float, y: float, s: str, fontdict: dict[str, Any] | None = ..., **kwargs) -> Text: ...
def gca() -> Axes: ...
def gci() -> ScalarMappable | None: ...
def ginput(n: int = ..., timeout: float = ..., show_clicks: bool = ..., mouse_add: MouseButton = ..., mouse_pop: MouseButton = ..., mouse_stop: MouseButton = ...) -> list[tuple[int, int]]: ...
def subplots_adjust(left: float | None = ..., bottom: float | None = ..., right: float | None = ..., top: float | None = ..., wspace: float | None = ..., hspace: float | None = ...) -> None: ...
def suptitle(t: str, **kwargs) -> Text: ...
def tight_layout(*, pad: float = ..., h_pad: float | None = ..., w_pad: float | None = ..., rect: tuple[float, float, float, float] | None = ...) -> None: ...
def waitforbuttonpress(timeout: float = ...) -> None | bool: ...
def acorr(x: ArrayLike, *, data: Incomplete | None = ..., **kwargs) -> tuple[np.ndarray, np.ndarray, LineCollection | Line2D, Line2D | None]: ...
def angle_spectrum(x: ArrayLike, Fs: float | None = ..., Fc: int | None = ..., window: Callable[[ArrayLike], ArrayLike] | ArrayLike | None = ..., pad_to: int | None = ..., sides: Literal['default', 'onesided', 'twosided'] | None = ..., *, data: Incomplete | None = ..., **kwargs) -> tuple[np.ndarray, np.ndarray, Line2D]: ...
def annotate(text: str, xy: tuple[float, float], xytext: tuple[float, float] | None = ..., xycoords: str | Artist | Transform | Callable[[RendererBase], Bbox | Transform] | tuple[float, float] = ..., textcoords: str | Artist | Transform | Callable[[RendererBase], Bbox | Transform] | tuple[float, float] | None = ..., arrowprops: dict[str, Any] | None = ..., annotation_clip: bool | None = ..., **kwargs) -> Annotation: ...
def arrow(x: float, y: float, dx: float, dy: float, **kwargs) -> FancyArrow: ...
def autoscale(enable: bool = ..., axis: Literal['both', 'x', 'y'] = ..., tight: bool | None = ...) -> None: ...
def axhline(y: float = ..., xmin: float = ..., xmax: float = ..., **kwargs) -> Line2D: ...
def axhspan(ymin: float, ymax: float, xmin: float = ..., xmax: float = ..., **kwargs) -> Polygon: ...
def axis(arg: tuple[float, float, float, float] | bool | str | None = ..., *, emit: bool = ..., **kwargs) -> tuple[float, float, float, float]: ...
def axline(xy1: tuple[float, float], xy2: tuple[float, float] | None = ..., *, slope: float | None = ..., **kwargs) -> Line2D: ...
def axvline(x: float = ..., ymin: float = ..., ymax: float = ..., **kwargs) -> Line2D: ...
def axvspan(xmin: float, xmax: float, ymin: float = ..., ymax: float = ..., **kwargs) -> Polygon: ...
def bar(x: float | ArrayLike, height: float | ArrayLike, width: float | ArrayLike = ..., bottom: float | ArrayLike | None = ..., *, align: Literal['center', 'edge'] = ..., data: Incomplete | None = ..., **kwargs) -> BarContainer: ...
def barbs(*args, data: Incomplete | None = ..., **kwargs) -> Barbs: ...
def barh(y: float | ArrayLike, width: float | ArrayLike, height: float | ArrayLike = ..., left: float | ArrayLike | None = ..., *, align: Literal['center', 'edge'] = ..., data: Incomplete | None = ..., **kwargs) -> BarContainer: ...
def bar_label(container: BarContainer, labels: ArrayLike | None = ..., *, fmt: str | Callable[[float], str] = ..., label_type: Literal['center', 'edge'] = ..., padding: float = ..., **kwargs) -> list[Annotation]: ...
def boxplot(x: ArrayLike | Sequence[ArrayLike], notch: bool | None = ..., sym: str | None = ..., vert: bool | None = ..., whis: float | tuple[float, float] | None = ..., positions: ArrayLike | None = ..., widths: float | ArrayLike | None = ..., patch_artist: bool | None = ..., bootstrap: int | None = ..., usermedians: ArrayLike | None = ..., conf_intervals: ArrayLike | None = ..., meanline: bool | None = ..., showmeans: bool | None = ..., showcaps: bool | None = ..., showbox: bool | None = ..., showfliers: bool | None = ..., boxprops: dict[str, Any] | None = ..., labels: Sequence[str] | None = ..., flierprops: dict[str, Any] | None = ..., medianprops: dict[str, Any] | None = ..., meanprops: dict[str, Any] | None = ..., capprops: dict[str, Any] | None = ..., whiskerprops: dict[str, Any] | None = ..., manage_ticks: bool = ..., autorange: bool = ..., zorder: float | None = ..., capwidths: float | ArrayLike | None = ..., *, data: Incomplete | None = ...) -> dict[str, Any]: ...
def broken_barh(xranges: Sequence[tuple[float, float]], yrange: tuple[float, float], *, data: Incomplete | None = ..., **kwargs) -> BrokenBarHCollection: ...
def clabel(CS: ContourSet, levels: ArrayLike | None = ..., **kwargs) -> list[Text]: ...
def cohere(x: ArrayLike, y: ArrayLike, NFFT: int = ..., Fs: float = ..., Fc: int = ..., detrend: Literal['none', 'mean', 'linear'] | Callable[[ArrayLike], ArrayLike] = ..., window: Callable[[ArrayLike], ArrayLike] | ArrayLike = ..., noverlap: int = ..., pad_to: int | None = ..., sides: Literal['default', 'onesided', 'twosided'] = ..., scale_by_freq: bool | None = ..., *, data: Incomplete | None = ..., **kwargs) -> tuple[np.ndarray, np.ndarray]: ...
def contour(*args, data: Incomplete | None = ..., **kwargs) -> QuadContourSet: ...
def contourf(*args, data: Incomplete | None = ..., **kwargs) -> QuadContourSet: ...
def csd(x: ArrayLike, y: ArrayLike, NFFT: int | None = ..., Fs: float | None = ..., Fc: int | None = ..., detrend: Literal['none', 'mean', 'linear'] | Callable[[ArrayLike], ArrayLike] | None = ..., window: Callable[[ArrayLike], ArrayLike] | ArrayLike | None = ..., noverlap: int | None = ..., pad_to: int | None = ..., sides: Literal['default', 'onesided', 'twosided'] | None = ..., scale_by_freq: bool | None = ..., return_line: bool | None = ..., *, data: Incomplete | None = ..., **kwargs) -> tuple[np.ndarray, np.ndarray] | tuple[np.ndarray, np.ndarray, Line2D]: ...
def ecdf(x: ArrayLike, weights: ArrayLike | None = ..., *, complementary: bool = ..., orientation: Literal['vertical', 'horizonatal'] = ..., compress: bool = ..., data: Incomplete | None = ..., **kwargs) -> Line2D: ...
def errorbar(x: float | ArrayLike, y: float | ArrayLike, yerr: float | ArrayLike | None = ..., xerr: float | ArrayLike | None = ..., fmt: str = ..., ecolor: ColorType | None = ..., elinewidth: float | None = ..., capsize: float | None = ..., barsabove: bool = ..., lolims: bool | ArrayLike = ..., uplims: bool | ArrayLike = ..., xlolims: bool | ArrayLike = ..., xuplims: bool | ArrayLike = ..., errorevery: int | tuple[int, int] = ..., capthick: float | None = ..., *, data: Incomplete | None = ..., **kwargs) -> ErrorbarContainer: ...
def eventplot(positions: ArrayLike | Sequence[ArrayLike], orientation: Literal['horizontal', 'vertical'] = ..., lineoffsets: float | Sequence[float] = ..., linelengths: float | Sequence[float] = ..., linewidths: float | Sequence[float] | None = ..., colors: ColorType | Sequence[ColorType] | None = ..., alpha: float | Sequence[float] | None = ..., linestyles: LineStyleType | Sequence[LineStyleType] = ..., *, data: Incomplete | None = ..., **kwargs) -> EventCollection: ...
def fill(*args, data: Incomplete | None = ..., **kwargs) -> list[Polygon]: ...
def fill_between(x: ArrayLike, y1: ArrayLike | float, y2: ArrayLike | float = ..., where: Sequence[bool] | None = ..., interpolate: bool = ..., step: Literal['pre', 'post', 'mid'] | None = ..., *, data: Incomplete | None = ..., **kwargs) -> PolyCollection: ...
def fill_betweenx(y: ArrayLike, x1: ArrayLike | float, x2: ArrayLike | float = ..., where: Sequence[bool] | None = ..., step: Literal['pre', 'post', 'mid'] | None = ..., interpolate: bool = ..., *, data: Incomplete | None = ..., **kwargs) -> PolyCollection: ...
def grid(visible: bool | None = ..., which: Literal['major', 'minor', 'both'] = ..., axis: Literal['both', 'x', 'y'] = ..., **kwargs) -> None: ...
def hexbin(x: ArrayLike, y: ArrayLike, C: ArrayLike | None = ..., gridsize: int | tuple[int, int] = ..., bins: Literal['log'] | int | Sequence[float] | None = ..., xscale: Literal['linear', 'log'] = ..., yscale: Literal['linear', 'log'] = ..., extent: tuple[float, float, float, float] | None = ..., cmap: str | Colormap | None = ..., norm: str | Normalize | None = ..., vmin: float | None = ..., vmax: float | None = ..., alpha: float | None = ..., linewidths: float | None = ..., edgecolors: Literal['face', 'none'] | ColorType = ..., reduce_C_function: Callable[[np.ndarray | list[float]], float] = ..., mincnt: int | None = ..., marginals: bool = ..., *, data: Incomplete | None = ..., **kwargs) -> PolyCollection: ...
def hist(x: ArrayLike | Sequence[ArrayLike], bins: int | Sequence[float] | str | None = ..., range: tuple[float, float] | None = ..., density: bool = ..., weights: ArrayLike | None = ..., cumulative: bool | float = ..., bottom: ArrayLike | float | None = ..., histtype: Literal['bar', 'barstacked', 'step', 'stepfilled'] = ..., align: Literal['left', 'mid', 'right'] = ..., orientation: Literal['vertical', 'horizontal'] = ..., rwidth: float | None = ..., log: bool = ..., color: ColorType | Sequence[ColorType] | None = ..., label: str | Sequence[str] | None = ..., stacked: bool = ..., *, data: Incomplete | None = ..., **kwargs) -> tuple[np.ndarray | list[np.ndarray], np.ndarray, BarContainer | Polygon | list[BarContainer | Polygon]]: ...
def stairs(values: ArrayLike, edges: ArrayLike | None = ..., *, orientation: Literal['vertical', 'horizontal'] = ..., baseline: float | ArrayLike | None = ..., fill: bool = ..., data: Incomplete | None = ..., **kwargs) -> StepPatch: ...
def hist2d(x: ArrayLike, y: ArrayLike, bins: None | int | tuple[int, int] | ArrayLike | tuple[ArrayLike, ArrayLike] = ..., range: ArrayLike | None = ..., density: bool = ..., weights: ArrayLike | None = ..., cmin: float | None = ..., cmax: float | None = ..., *, data: Incomplete | None = ..., **kwargs) -> tuple[np.ndarray, np.ndarray, np.ndarray, QuadMesh]: ...
def hlines(y: float | ArrayLike, xmin: float | ArrayLike, xmax: float | ArrayLike, colors: ColorType | Sequence[ColorType] | None = ..., linestyles: LineStyleType = ..., label: str = ..., *, data: Incomplete | None = ..., **kwargs) -> LineCollection: ...
def imshow(X: ArrayLike | PIL.Image.Image, cmap: str | Colormap | None = ..., norm: str | Normalize | None = ..., *, aspect: Literal['equal', 'auto'] | float | None = ..., interpolation: str | None = ..., alpha: float | ArrayLike | None = ..., vmin: float | None = ..., vmax: float | None = ..., origin: Literal['upper', 'lower'] | None = ..., extent: tuple[float, float, float, float] | None = ..., interpolation_stage: Literal['data', 'rgba'] | None = ..., filternorm: bool = ..., filterrad: float = ..., resample: bool | None = ..., url: str | None = ..., data: Incomplete | None = ..., **kwargs) -> AxesImage: ...
def legend(*args, **kwargs) -> Legend: ...
def locator_params(axis: Literal['both', 'x', 'y'] = ..., tight: bool | None = ..., **kwargs) -> None: ...
def loglog(*args, **kwargs) -> list[Line2D]: ...
def magnitude_spectrum(x: ArrayLike, Fs: float | None = ..., Fc: int | None = ..., window: Callable[[ArrayLike], ArrayLike] | ArrayLike | None = ..., pad_to: int | None = ..., sides: Literal['default', 'onesided', 'twosided'] | None = ..., scale: Literal['default', 'linear', 'dB'] | None = ..., *, data: Incomplete | None = ..., **kwargs) -> tuple[np.ndarray, np.ndarray, Line2D]: ...
def margins(*margins: float, x: float | None = ..., y: float | None = ..., tight: bool | None = ...) -> tuple[float, float] | None: ...
def minorticks_off() -> None: ...
def minorticks_on() -> None: ...
def pcolor(*args: ArrayLike, shading: Literal['flat', 'nearest', 'auto'] | None = ..., alpha: float | None = ..., norm: str | Normalize | None = ..., cmap: str | Colormap | None = ..., vmin: float | None = ..., vmax: float | None = ..., data: Incomplete | None = ..., **kwargs) -> Collection: ...
def pcolormesh(*args: ArrayLike, alpha: float | None = ..., norm: str | Normalize | None = ..., cmap: str | Colormap | None = ..., vmin: float | None = ..., vmax: float | None = ..., shading: Literal['flat', 'nearest', 'gouraud', 'auto'] | None = ..., antialiased: bool = ..., data: Incomplete | None = ..., **kwargs) -> QuadMesh: ...
def phase_spectrum(x: ArrayLike, Fs: float | None = ..., Fc: int | None = ..., window: Callable[[ArrayLike], ArrayLike] | ArrayLike | None = ..., pad_to: int | None = ..., sides: Literal['default', 'onesided', 'twosided'] | None = ..., *, data: Incomplete | None = ..., **kwargs) -> tuple[np.ndarray, np.ndarray, Line2D]: ...
def pie(x: ArrayLike, explode: ArrayLike | None = ..., labels: Sequence[str] | None = ..., colors: ColorType | Sequence[ColorType] | None = ..., autopct: str | Callable[[float], str] | None = ..., pctdistance: float = ..., shadow: bool = ..., labeldistance: float | None = ..., startangle: float = ..., radius: float = ..., counterclock: bool = ..., wedgeprops: dict[str, Any] | None = ..., textprops: dict[str, Any] | None = ..., center: tuple[float, float] = ..., frame: bool = ..., rotatelabels: bool = ..., *, normalize: bool = ..., hatch: str | Sequence[str] | None = ..., data: Incomplete | None = ...) -> tuple[list[Wedge], list[Text]] | tuple[list[Wedge], list[Text], list[Text]]: ...
def plot(*args: float | ArrayLike | str, scalex: bool = ..., scaley: bool = ..., data: Incomplete | None = ..., **kwargs) -> list[Line2D]: ...
def plot_date(x: ArrayLike, y: ArrayLike, fmt: str = ..., tz: str | datetime.tzinfo | None = ..., xdate: bool = ..., ydate: bool = ..., *, data: Incomplete | None = ..., **kwargs) -> list[Line2D]: ...
def psd(x: ArrayLike, NFFT: int | None = ..., Fs: float | None = ..., Fc: int | None = ..., detrend: Literal['none', 'mean', 'linear'] | Callable[[ArrayLike], ArrayLike] | None = ..., window: Callable[[ArrayLike], ArrayLike] | ArrayLike | None = ..., noverlap: int | None = ..., pad_to: int | None = ..., sides: Literal['default', 'onesided', 'twosided'] | None = ..., scale_by_freq: bool | None = ..., return_line: bool | None = ..., *, data: Incomplete | None = ..., **kwargs) -> tuple[np.ndarray, np.ndarray] | tuple[np.ndarray, np.ndarray, Line2D]: ...
def quiver(*args, data: Incomplete | None = ..., **kwargs) -> Quiver: ...
def quiverkey(Q: Quiver, X: float, Y: float, U: float, label: str, **kwargs) -> QuiverKey: ...
def scatter(x: float | ArrayLike, y: float | ArrayLike, s: float | ArrayLike | None = ..., c: ArrayLike | Sequence[ColorType] | ColorType | None = ..., marker: MarkerType | None = ..., cmap: str | Colormap | None = ..., norm: str | Normalize | None = ..., vmin: float | None = ..., vmax: float | None = ..., alpha: float | None = ..., linewidths: float | Sequence[float] | None = ..., *, edgecolors: Literal['face', 'none'] | ColorType | Sequence[ColorType] | None = ..., plotnonfinite: bool = ..., data: Incomplete | None = ..., **kwargs) -> PathCollection: ...
def semilogx(*args, **kwargs) -> list[Line2D]: ...
def semilogy(*args, **kwargs) -> list[Line2D]: ...
def specgram(x: ArrayLike, NFFT: int | None = ..., Fs: float | None = ..., Fc: int | None = ..., detrend: Literal['none', 'mean', 'linear'] | Callable[[ArrayLike], ArrayLike] | None = ..., window: Callable[[ArrayLike], ArrayLike] | ArrayLike | None = ..., noverlap: int | None = ..., cmap: str | Colormap | None = ..., xextent: tuple[float, float] | None = ..., pad_to: int | None = ..., sides: Literal['default', 'onesided', 'twosided'] | None = ..., scale_by_freq: bool | None = ..., mode: Literal['default', 'psd', 'magnitude', 'angle', 'phase'] | None = ..., scale: Literal['default', 'linear', 'dB'] | None = ..., vmin: float | None = ..., vmax: float | None = ..., *, data: Incomplete | None = ..., **kwargs) -> tuple[np.ndarray, np.ndarray, np.ndarray, AxesImage]: ...
def spy(Z: ArrayLike, precision: float | Literal['present'] = ..., marker: str | None = ..., markersize: float | None = ..., aspect: Literal['equal', 'auto'] | float | None = ..., origin: Literal['upper', 'lower'] = ..., **kwargs) -> AxesImage: ...
def stackplot(x, *args, labels=..., colors: Incomplete | None = ..., baseline: str = ..., data: Incomplete | None = ..., **kwargs): ...
def stem(*args: ArrayLike | str, linefmt: str | None = ..., markerfmt: str | None = ..., basefmt: str | None = ..., bottom: float = ..., label: str | None = ..., orientation: Literal['vertical', 'horizontal'] = ..., data: Incomplete | None = ...) -> StemContainer: ...
def step(x: ArrayLike, y: ArrayLike, *args, where: Literal['pre', 'post', 'mid'] = ..., data: Incomplete | None = ..., **kwargs) -> list[Line2D]: ...
def streamplot(x, y, u, v, density: int = ..., linewidth: Incomplete | None = ..., color: Incomplete | None = ..., cmap: Incomplete | None = ..., norm: Incomplete | None = ..., arrowsize: int = ..., arrowstyle: str = ..., minlength: float = ..., transform: Incomplete | None = ..., zorder: Incomplete | None = ..., start_points: Incomplete | None = ..., maxlength: float = ..., integration_direction: str = ..., broken_streamlines: bool = ..., *, data: Incomplete | None = ...): ...
def table(cellText: Incomplete | None = ..., cellColours: Incomplete | None = ..., cellLoc: str = ..., colWidths: Incomplete | None = ..., rowLabels: Incomplete | None = ..., rowColours: Incomplete | None = ..., rowLoc: str = ..., colLabels: Incomplete | None = ..., colColours: Incomplete | None = ..., colLoc: str = ..., loc: str = ..., bbox: Incomplete | None = ..., edges: str = ..., **kwargs): ...
def text(x: float, y: float, s: str, fontdict: dict[str, Any] | None = ..., **kwargs) -> Text: ...
def tick_params(axis: Literal['both', 'x', 'y'] = ..., **kwargs) -> None: ...
def ticklabel_format(*, axis: Literal['both', 'x', 'y'] = ..., style: Literal['', 'sci', 'scientific', 'plain'] = ..., scilimits: tuple[int, int] | None = ..., useOffset: bool | float | None = ..., useLocale: bool | None = ..., useMathText: bool | None = ...) -> None: ...
def tricontour(*args, **kwargs): ...
def tricontourf(*args, **kwargs): ...
def tripcolor(*args, alpha: float = ..., norm: Incomplete | None = ..., cmap: Incomplete | None = ..., vmin: Incomplete | None = ..., vmax: Incomplete | None = ..., shading: str = ..., facecolors: Incomplete | None = ..., **kwargs): ...
def triplot(*args, **kwargs): ...
def violinplot(dataset: ArrayLike | Sequence[ArrayLike], positions: ArrayLike | None = ..., vert: bool = ..., widths: float | ArrayLike = ..., showmeans: bool = ..., showextrema: bool = ..., showmedians: bool = ..., quantiles: Sequence[float | Sequence[float]] | None = ..., points: int = ..., bw_method: Literal['scott', 'silverman'] | float | Callable[[GaussianKDE], float] | None = ..., *, data: Incomplete | None = ...) -> dict[str, Collection]: ...
def vlines(x: float | ArrayLike, ymin: float | ArrayLike, ymax: float | ArrayLike, colors: ColorType | Sequence[ColorType] | None = ..., linestyles: LineStyleType = ..., label: str = ..., *, data: Incomplete | None = ..., **kwargs) -> LineCollection: ...
def xcorr(x: ArrayLike, y: ArrayLike, normed: bool = ..., detrend: Callable[[ArrayLike], ArrayLike] = ..., usevlines: bool = ..., maxlags: int = ..., *, data: Incomplete | None = ..., **kwargs) -> tuple[np.ndarray, np.ndarray, LineCollection | Line2D, Line2D | None]: ...
def sci(im: ScalarMappable) -> None: ...
def title(label: str, fontdict: dict[str, Any] | None = ..., loc: Literal['left', 'center', 'right'] | None = ..., pad: float | None = ..., *, y: float | None = ..., **kwargs) -> Text: ...
def xlabel(xlabel: str, fontdict: dict[str, Any] | None = ..., labelpad: float | None = ..., *, loc: Literal['left', 'center', 'right'] | None = ..., **kwargs) -> Text: ...
def ylabel(ylabel: str, fontdict: dict[str, Any] | None = ..., labelpad: float | None = ..., *, loc: Literal['bottom', 'center', 'top'] | None = ..., **kwargs) -> Text: ...
def xscale(value: str | ScaleBase, **kwargs) -> None: ...
def yscale(value: str | ScaleBase, **kwargs) -> None: ...
def autumn() -> None: ...
def bone() -> None: ...
def cool() -> None: ...
def copper() -> None: ...
def flag() -> None: ...
def gray() -> None: ...
def hot() -> None: ...
def hsv() -> None: ...
def jet() -> None: ...
def pink() -> None: ...
def prism() -> None: ...
def spring() -> None: ...
def summer() -> None: ...
def winter() -> None: ...
def magma() -> None: ...
def inferno() -> None: ...
def plasma() -> None: ...
def viridis() -> None: ...
def nipy_spectral() -> None: ...
