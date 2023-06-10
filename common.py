"""Common stuff..."""
from collections.abc import Callable
from typing import Protocol, Any, TypeVar


class SupportsLessThan(Protocol):
	"""Protocol required by several classes."""
	
	def __lt__(self, other: Any) -> bool:
		...


SupportsLessThanT = TypeVar("SupportsLessThanT", bound=SupportsLessThan)


KeyFunction = Callable[[SupportsLessThanT], SupportsLessThanT]
