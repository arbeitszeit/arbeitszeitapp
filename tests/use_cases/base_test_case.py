from typing import Any, Dict, Generic, Type, TypeVar
from unittest import TestCase

from tests.data_generators import (
    AccountantGenerator,
    CompanyGenerator,
    CooperationGenerator,
    MemberGenerator,
    PlanGenerator,
)
from tests.datetime_service import FakeDatetimeService

from .balance_checker import BalanceChecker
from .dependency_injection import get_dependency_injector
from .price_checker import PriceChecker

T = TypeVar("T")


# This class is a descriptor. Check
# https://docs.python.org/3/howto/descriptor.html for more information
# on descriptors.
class _lazy_property(Generic[T]):
    def __init__(self, cls: Type[T]):
        """Implement a lazy property for the BaseTestCase.  If the
        implementor asks for this attribute then it is generated on
        demand and cached.
        """
        self.cls = cls

    def __set_name__(self, owner, name: str) -> None:
        self._attribute_name = name

    def __get__(self, obj: Any, objtype=None) -> T:
        cache = obj._lazy_property_cache
        instance = cache.get(self._attribute_name)
        if instance is None:
            instance = obj.injector.get(self.cls)
            cache[self._attribute_name] = instance
        return instance

    def __set__(self, obj: Any, value: T) -> None:
        raise Exception("This attribute is read-only")


class BaseTestCase(TestCase):
    "Use case unit tests should inherit from this class."

    def setUp(self) -> None:
        super().setUp()
        self._lazy_property_cache: Dict[str, Any] = dict()
        self.injector = get_dependency_injector()

    def tearDown(self) -> None:
        self._lazy_property_cache = dict()
        super().tearDown()

    # It would be nice to have the following list sorted
    # alphabetically
    accountant_generator = _lazy_property(AccountantGenerator)
    balance_checker = _lazy_property(BalanceChecker)
    company_generator = _lazy_property(CompanyGenerator)
    coop_generator = _lazy_property(CooperationGenerator)
    cooperation_generator = _lazy_property(CooperationGenerator)
    datetime_service = _lazy_property(FakeDatetimeService)
    member_generator = _lazy_property(MemberGenerator)
    plan_generator = _lazy_property(PlanGenerator)
    price_checker = _lazy_property(PriceChecker)
