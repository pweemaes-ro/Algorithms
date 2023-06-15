"""Another sorting algorithm..."""
from collections.abc import Callable
from operator import gt, lt
from typing import Optional

from common import SupportsLessThanT


def selection_sort(sequence: list[SupportsLessThanT],
                   key: Optional[Callable[[SupportsLessThanT],
                                 SupportsLessThanT]] = None,
                   reverse: bool = False) -> None:
	"""Selection Sort is a simple and intuitive sorting algorithm that works by
	repeatedly selecting the minimum element from an unsorted subarray and
	swapping it with the element at the beginning of the subarray. This process
	is repeated for each element in the array until the entire array is sorted.
	At each iteration, Selection Sort finds the minimum element in the
	remaining unsorted subarray and swaps it with the element at the current
	index."""
	
	# Note: selection_sort is UNSTABLE by nature, and attempting to make it
	# stable would transform it in another sorting algorithm (say, insertion
	# sort).

	n = len(sequence)

	if reverse:
		compare_operator = gt
	else:
		compare_operator = lt
	
	if key:
		keys = [*map(key, sequence)]
	else:
		keys = sequence
	
	for i in range(n - 1):
		s = i
		for j in range(i + 1, n):
			if compare_operator(keys[j], keys[s]):
				s = j
		sequence[s], sequence[i] = sequence[i], sequence[s]
		if keys is not sequence:
			keys[s], keys[i] = keys[i], keys[s]
