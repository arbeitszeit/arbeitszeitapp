from _typeshed import Incomplete

def clean_datetime_format_for_strptime(formats): ...

class UnsetValue:
    def __bool__(self) -> bool: ...
    def __nonzero__(self): ...

unset_value: Incomplete

class WebobInputWrapper:
    def __init__(self, multidict) -> None: ...
    def __iter__(self): ...
    def __len__(self) -> int: ...
    def __contains__(self, name) -> bool: ...
    def getlist(self, name): ...
