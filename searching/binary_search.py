"""Binary search """
from collections.abc import Sequence
from typing import Optional

from common import SupportsLessThanT


def binary_search(data: Sequence[SupportsLessThanT],
                  target: SupportsLessThanT,
                  first: int = 0,
                  last: Optional[int] = None) -> Optional[int]:
	"""Return the 0-based index of *target* in *data* if *target* found in
	*data*, else return *None*. The *data* is assumed to be sorted in ascending
	order!"""
	
	if last is None:
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


def binary_search_recursive(data: Sequence[SupportsLessThanT],
                            target: SupportsLessThanT,
                            first: int = 0,
                            last: Optional[int] = None) -> Optional[int]:
	"""Return the 0-based index of *target* in *data* if *target* found in
	*data*, else return *None*. The *data* is assumed to be sorted in ascending
	order!"""
	
	if last is None:
		last = len(data) - 1

	if last - first < 0:
		return None

	mid_point = (last + first) // 2
	mid_value = data[mid_point]
	if mid_value == target:
		return mid_point
	elif target < mid_value:
		return binary_search_recursive(data, target, first, mid_point - 1)
	else:
		return binary_search_recursive(data, target, mid_point + 1, last)
