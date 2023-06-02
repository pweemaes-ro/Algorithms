"""Common stuff..."""
from typing import Protocol, Any, TypeVar


class SupportsLessThan(Protocol):
	"""Protocol required by several classes."""
	
	def __lt__(self, other: Any) -> bool:
		...


class SupportsLessThanOrEqual(Protocol):
	"""Protocol required by several classes."""
	
	def __eq__(self, other: Any) -> bool:
		...
	
	def __lt__(self, other: Any) -> bool:
		...

	def __le__(self, other: Any) -> bool:
		...


SupportsLessThanT = TypeVar("SupportsLessThanT", bound=SupportsLessThan)
SupportsLessThanOrEqualT = TypeVar("SupportsLessThanOrEqualT",
                                   bound=SupportsLessThanOrEqual)
