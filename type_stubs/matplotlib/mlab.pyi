from _typeshed import Incomplete
from matplotlib import cbook as cbook

def window_hanning(x): ...
def window_none(x): ...
def detrend(x, key: Incomplete | None = ..., axis: Incomplete | None = ...): ...
def detrend_mean(x, axis: Incomplete | None = ...): ...
def detrend_none(x, axis: Incomplete | None = ...): ...
def detrend_linear(y): ...
def psd(x, NFFT: Incomplete | None = ..., Fs: Incomplete | None = ..., detrend: Incomplete | None = ..., window: Incomplete | None = ..., noverlap: Incomplete | None = ..., pad_to: Incomplete | None = ..., sides: Incomplete | None = ..., scale_by_freq: Incomplete | None = ...): ...
def csd(x, y, NFFT: Incomplete | None = ..., Fs: Incomplete | None = ..., detrend: Incomplete | None = ..., window: Incomplete | None = ..., noverlap: Incomplete | None = ..., pad_to: Incomplete | None = ..., sides: Incomplete | None = ..., scale_by_freq: Incomplete | None = ...): ...

complex_spectrum: Incomplete
magnitude_spectrum: Incomplete
angle_spectrum: Incomplete
phase_spectrum: Incomplete

def specgram(x, NFFT: Incomplete | None = ..., Fs: Incomplete | None = ..., detrend: Incomplete | None = ..., window: Incomplete | None = ..., noverlap: Incomplete | None = ..., pad_to: Incomplete | None = ..., sides: Incomplete | None = ..., scale_by_freq: Incomplete | None = ..., mode: Incomplete | None = ...): ...
def cohere(x, y, NFFT: int = ..., Fs: int = ..., detrend=..., window=..., noverlap: int = ..., pad_to: Incomplete | None = ..., sides: str = ..., scale_by_freq: Incomplete | None = ...): ...

class GaussianKDE:
    dataset: Incomplete
    covariance_factor: Incomplete
    factor: Incomplete
    data_covariance: Incomplete
    data_inv_cov: Incomplete
    covariance: Incomplete
    inv_cov: Incomplete
    norm_factor: Incomplete
    def __init__(self, dataset, bw_method: Incomplete | None = ...) -> None: ...
    def scotts_factor(self): ...
    def silverman_factor(self): ...
    covariance_factor = scotts_factor
    def evaluate(self, points): ...
    __call__ = evaluate
