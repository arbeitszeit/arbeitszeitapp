from _typeshed import Incomplete
from deepdiff.helper import RemapDict as RemapDict, dict_ as dict_, get_type as get_type, literal_eval_extended as literal_eval_extended, notpresent as notpresent, np as np, numpy_numbers as numpy_numbers, short_repr as short_repr, strings as strings
from deepdiff.path import stringify_element as stringify_element
from ordered_set import OrderedSet

logger: Incomplete
FORCE_DEFAULT: str
UP_DOWN: Incomplete
REPORT_KEYS: Incomplete
CUSTOM_FIELD: str

class DoesNotExist(Exception): ...

class ResultDict(RemapDict):
    def remove_empty_keys(self) -> None: ...

class PrettyOrderedSet(OrderedSet): ...

class TreeResult(ResultDict):
    def __init__(self) -> None: ...
    def mutual_add_removes_to_become_value_changes(self) -> None: ...
    def __getitem__(self, item): ...
    def __len__(self) -> int: ...

class TextResult(ResultDict):
    ADD_QUOTES_TO_STRINGS: bool
    verbose_level: Incomplete
    def __init__(self, tree_results: Incomplete | None = ..., verbose_level: int = ...) -> None: ...

class DeltaResult(TextResult):
    ADD_QUOTES_TO_STRINGS: bool
    ignore_order: Incomplete
    always_include_values: Incomplete
    def __init__(self, tree_results: Incomplete | None = ..., ignore_order: Incomplete | None = ..., always_include_values: bool = ...) -> None: ...

class DiffLevel:
    t1: Incomplete
    t2: Incomplete
    down: Incomplete
    up: Incomplete
    report_type: Incomplete
    additional: Incomplete
    t1_child_rel: Incomplete
    t2_child_rel: Incomplete
    verbose_level: Incomplete
    def __init__(self, t1, t2, down: Incomplete | None = ..., up: Incomplete | None = ..., report_type: Incomplete | None = ..., child_rel1: Incomplete | None = ..., child_rel2: Incomplete | None = ..., additional: Incomplete | None = ..., verbose_level: int = ...) -> None: ...
    def __setattr__(self, key, value) -> None: ...
    def __iter__(self): ...
    @property
    def repetition(self): ...
    def auto_generate_child_rel(self, klass, param, param2: Incomplete | None = ...) -> None: ...
    @property
    def all_up(self): ...
    @property
    def all_down(self): ...
    def get_root_key(self, use_t2: bool = ...): ...
    def path(self, root: str = ..., force: Incomplete | None = ..., get_parent_too: bool = ..., use_t2: bool = ..., output_format: str = ...): ...
    def create_deeper(self, new_t1, new_t2, child_relationship_class, child_relationship_param: Incomplete | None = ..., child_relationship_param2: Incomplete | None = ..., report_type: Incomplete | None = ...): ...
    def branch_deeper(self, new_t1, new_t2, child_relationship_class, child_relationship_param: Incomplete | None = ..., child_relationship_param2: Incomplete | None = ..., report_type: Incomplete | None = ...): ...
    def copy(self): ...

class ChildRelationship:
    param_repr_format: Incomplete
    quote_str: Incomplete
    @staticmethod
    def create(klass, parent, child, param: Incomplete | None = ...): ...
    parent: Incomplete
    child: Incomplete
    param: Incomplete
    def __init__(self, parent, child, param: Incomplete | None = ...) -> None: ...
    def get_param_repr(self, force: Incomplete | None = ...): ...
    def stringify_param(self, force: Incomplete | None = ...): ...

class DictRelationship(ChildRelationship):
    param_repr_format: str
    quote_str: str

class NumpyArrayRelationship(ChildRelationship):
    param_repr_format: str
    quote_str: Incomplete

class SubscriptableIterableRelationship(DictRelationship): ...
class InaccessibleRelationship(ChildRelationship): ...
class SetRelationship(InaccessibleRelationship): ...

class NonSubscriptableIterableRelationship(InaccessibleRelationship):
    param_repr_format: str
    def get_param_repr(self, force: Incomplete | None = ...): ...

class AttributeRelationship(ChildRelationship):
    param_repr_format: str
