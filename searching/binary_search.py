"""Binary search """
from collections.abc import Sequence
from typing import Optional

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


if __name__ == "__main__":
	
	def binary_search_test() -> None:
		"""Test binary_search function."""
		
		search_func = binary_search
		data = list(range(10))
		for target in data:
			assert search_func(data, target) == target
		
		assert search_func([], 1) is None
		assert search_func([], 0) is None
		
		not_in_data = (-1, 23)
		for target in not_in_data:
			assert search_func(data, target) is None

	binary_search_test()
