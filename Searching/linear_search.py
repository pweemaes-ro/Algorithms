"""Linear search algorithm,"""
from collections.abc import Sequence
from typing import Optional

from common import SupportsLessThanT


def linear_search(data: Sequence[SupportsLessThanT],
                  target: SupportsLessThanT) -> Optional[int]:
	"""Return the 0-based index of *target* in *data* if *target* found in
	*data*, else return *None*"""
	
	for i in range(len(data)):
		if data[i] == target:
			return i
	
	return None


if __name__ == "__main__":
	def linear_search_test() -> None:
		"""Test binary_search function."""
		
		search_func = linear_search
		data = list(range(10))
		for target in data:
			assert search_func(data, target) == target
		
		assert search_func([], 1) is None
		assert search_func([], 0) is None
		
		not_in_data = (-1, 23)
		for target in not_in_data:
			assert search_func(data, target) is None
	
	
	linear_search_test()
