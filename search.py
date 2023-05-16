"""Some search algorithms"""
from typing import Sequence, Optional, Protocol, Any, Callable, \
	TypeAlias


class Comparable(Protocol):
	"""Protocal for Comparable types"""

	def __gt__(self, other: Any) -> bool:
		pass


SearchFunc: TypeAlias = \
	Callable[[Sequence[Comparable], Comparable], Optional[int]]
ExistsFunc: TypeAlias = \
	Callable[[Sequence[Comparable], Comparable], bool]


def linear_search(data: Sequence[Comparable], target: Comparable) \
	-> Optional[int]:
	"""Return the 0-based index of *target* in *data* if *target* found in
	*data*, else return *None*"""
	
	for i in range(len(data)):
		if data[i] == target:
			return i
	return None


def binary_search(data: Sequence[Comparable], target: Comparable) \
	-> Optional[int]:
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


def binary_search_r(data: Sequence[Comparable],
                    target: Comparable,
                    first: int = 0,
                    last: Optional[int] = None) -> Optional[int]:
	"""Recursive version of binary search. Return the 0-based index of *target*
	in *data* if *target* found in *data*, else return *None*. The *data* is
	assumed to be sorted in ascending order!"""

	if last is None:
		last = len(data) - 1

	if last - first >= 0:
		mid_point = (last + first) // 2
		mid_value = data[mid_point]
		if mid_value == target:
			return mid_point
		if target > mid_value:
			return binary_search_r(data, target, mid_point + 1, last)
		else:
			return binary_search_r(data, target, first, mid_point - 1)
	
	return None


def exists(data: Sequence[Comparable], target: Comparable) -> bool:
	"""Return True if *target* found in *data*, else return *False*. The *data*
	is assumed to be sorted in ascending order! Uses *binary_search* to
	determine if *target* exists in *data*."""
	return binary_search(data, target) is not None


def exists_r(data: Sequence[Comparable], target: Comparable) -> bool:
	"""Recursive version of exists. Return True if *target* found in *data*,
	else return *False*. The *data* is assumed to be sorted in ascending
	order!"""
	
	if len(data) == 0:
		return False

	mid_point = len(data) // 2
	value_at_midpoint = data[mid_point]
	if value_at_midpoint == target:
		return True
	if target > value_at_midpoint:
		return exists_r(data[mid_point + 1:], target)
	else:
		return exists_r(data[:mid_point], target)


if __name__ == "__main__":
	
	def _test_all_search_funcs() -> None:

		search_functions: tuple[SearchFunc, ...] = \
			(linear_search, binary_search, binary_search_r)
		
		for search_func in search_functions:
			data = list(range(10))
			for target in data:
				assert search_func(data, target) == target
			
			assert search_func([], 1) is None
			assert search_func([], 0) is None
			
			not_in_data = (-1, 23)
			for target in not_in_data:
				assert search_func(data, target) is None
	
	
	def _test_all_exists_functions() -> None:
		exists_functions: tuple[ExistsFunc, ...] = (exists, exists_r)
		
		for exists_func in exists_functions:
			data = list(range(10))
			for target in data:
				assert exists_func(data, target)
			
			assert not exists_func([], 1)
			assert not exists_func([], 0)
			
			not_in_data = (-1, 23)
			for target in not_in_data:
				assert not exists_func(data, target)
	
	
	def main() -> None:
		"""Run all tests."""
		
		_test_all_search_funcs()
		_test_all_exists_functions()

	main()
