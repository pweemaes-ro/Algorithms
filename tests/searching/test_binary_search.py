"""Test(s) for binary_search and binary_search_recursive."""

from collections.abc import Sequence
from typing import Optional, Protocol

from binary_search import binary_search, binary_search_recursive
from common import SupportsLessThanT


class _SearchFunc(Protocol):
	"""The best way to deal with 'complicated' function arguments (with
	default values). """
	
	def __call__(self,
	             data: Sequence[SupportsLessThanT],
	             target: SupportsLessThanT) -> Optional[int]:
		...

	# Use __name__ property if you want to print the search function's name
	# (no need for @abstractmethod, other than that PyCharm complains if
	# not... Mypy is happy without it).
	# @property
	# @abstractmethod
	# def __name__(self) -> str:
	# 	...


def _test_binary_search_func(search_func: _SearchFunc) -> None:
	"""Test the given function"""
	
	for i in range(10):
		data = list(range(i))
		for target in data:
			assert search_func(data, target) == target
		
		assert search_func([], 1) is None
		assert search_func([], 0) is None
		
		not_in_data = (-1, i)
		for target in not_in_data:
			assert search_func(data, target) is None


def test_binary_search() -> None:
	"""Test binary_search function."""
	
	_test_binary_search_func(binary_search)


def test_binary_search_recusive() -> None:
	"""Test binary_search_recursive function."""

	_test_binary_search_func(binary_search_recursive)
