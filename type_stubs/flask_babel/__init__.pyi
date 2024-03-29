from _typeshed import Incomplete
from babel import Locale
from babel.support import NullTranslations as NullTranslations, Translations as Translations
from collections.abc import Generator
from flask_babel.speaklater import LazyString as LazyString
from pytz import timezone
from typing import Callable, List, Optional, Union

class BabelConfiguration:
    default_locale: str
    default_timezone: str
    default_domain: str
    default_directories: List[str]
    translation_directories: List[str]
    instance: Babel
    locale_selector: Optional[Callable]
    timezone_selector: Optional[Callable]
    def __init__(self, default_locale, default_timezone, default_domain, default_directories, translation_directories, instance, locale_selector, timezone_selector) -> None: ...

def get_babel(app: Incomplete | None = ...) -> BabelConfiguration: ...

class Babel:
    default_date_formats: Incomplete
    date_formats: Incomplete
    def __init__(self, app: Incomplete | None = ..., date_formats: Incomplete | None = ..., configure_jinja: bool = ..., *args, **kwargs) -> None: ...
    def init_app(self, app, default_locale: str = ..., default_domain: str = ..., default_translation_directories: str = ..., default_timezone: str = ..., locale_selector: Incomplete | None = ..., timezone_selector: Incomplete | None = ...): ...
    def list_translations(self): ...
    @property
    def default_locale(self) -> Locale: ...
    @property
    def default_timezone(self) -> timezone: ...
    @property
    def domain(self) -> str: ...
    def domain_instance(self): ...

def get_translations() -> Union[Translations, NullTranslations]: ...
def get_locale() -> Optional[Locale]: ...
def get_timezone() -> Optional[timezone]: ...
def refresh() -> None: ...
def force_locale(locale) -> Generator[None, None, None]: ...
def to_user_timezone(datetime): ...
def to_utc(datetime): ...
def format_datetime(datetime: Incomplete | None = ..., format: Incomplete | None = ..., rebase: bool = ...): ...
def format_date(date: Incomplete | None = ..., format: Incomplete | None = ..., rebase: bool = ...): ...
def format_time(time: Incomplete | None = ..., format: Incomplete | None = ..., rebase: bool = ...): ...
def format_timedelta(datetime_or_timedelta, granularity: str = ..., add_direction: bool = ..., threshold: float = ...): ...
def format_number(number) -> str: ...
def format_decimal(number, format: Incomplete | None = ...) -> str: ...
def format_currency(number, currency, format: Incomplete | None = ..., currency_digits: bool = ..., format_type: str = ...) -> str: ...
def format_percent(number, format: Incomplete | None = ...) -> str: ...
def format_scientific(number, format: Incomplete | None = ...) -> str: ...

class Domain:
    domain: Incomplete
    cache: Incomplete
    def __init__(self, translation_directories: Incomplete | None = ..., domain: str = ...) -> None: ...
    @property
    def translation_directories(self): ...
    def as_default(self) -> None: ...
    def get_translations_cache(self, ctx): ...
    def get_translations(self): ...
    def gettext(self, string, **variables): ...
    def ngettext(self, singular, plural, num, **variables): ...
    def pgettext(self, context, string, **variables): ...
    def npgettext(self, context, singular, plural, num, **variables): ...
    def lazy_gettext(self, string, **variables): ...
    def lazy_ngettext(self, singular, plural, num, **variables): ...
    def lazy_pgettext(self, context, string, **variables): ...

def get_domain() -> Domain: ...
def gettext(*args, **kwargs) -> str: ...
def ngettext(*args, **kwargs) -> str: ...
def pgettext(*args, **kwargs) -> str: ...
def npgettext(*args, **kwargs) -> str: ...
def lazy_gettext(*args, **kwargs) -> LazyString: ...
def lazy_pgettext(*args, **kwargs) -> LazyString: ...
def lazy_ngettext(*args, **kwargs) -> LazyString: ...
def lazy_npgettext(*args, **kwargs) -> LazyString: ...
