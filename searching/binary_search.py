"""Binary search """
import time
from abc import abstractproperty, abstractmethod
from collections.abc import Sequence
from typing import Optional, Protocol

from common import SupportsLessThanT


def binary_search(data: Sequence[SupportsLessThanT],
                  target: SupportsLessThanT) -> Optional[int]:
	"""Return the 0-based index of *target* in *data* if *target* found in
	*data*, else return *None*. The *data* is assumed to be sorted in ascending
	order!"""
	
	first = 0
	last = len(data) - 1
	
	while last - first >= 0:
		mid_point = (last + first) // 2
		mid_value = data[mid_point]
		if mid_value == target:
			return mid_point
		if target > mid_value:
			first = mid_point + 1
		else:
			last = mid_point - 1
	
	return None


def _binary_search_recursive(data: Sequence[SupportsLessThanT],
                             target: SupportsLessThanT,
                             first: int,
                             last: int) -> Optional[int]:
	if last - first < 0:
		return None
	else:
		mid_point = (last + first) // 2
		mid_value = data[mid_point]
		if mid_value == target:
			return mid_point
		elif target < mid_value:
			return _binary_search_recursive(data, target, first, mid_point - 1)
		else:
			return _binary_search_recursive(data, target, mid_point + 1, last)


def binary_search_recursive(data: Sequence[SupportsLessThanT],
                            target: SupportsLessThanT) -> Optional[int]:
	"""Return the 0-based index of *target* in *data* if *target* found in
	*data*, else return *None*. The *data* is assumed to be sorted in ascending
	order!"""

	return _binary_search_recursive(data, target, 0, len(data) - 1)


if __name__ == "__main__":
	
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
	
	def _test_search_func(search_func: _SearchFunc) \
		-> None:
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
			
	def _binary_search_test() -> None:
		"""Test binary_search function."""
	
		for search_func in (binary_search, binary_search_recursive):
			_test_search_func(search_func)
			print(f"{search_func.__name__} completed without errors.")

	def main() -> None:
		_binary_search_test()

	main()
