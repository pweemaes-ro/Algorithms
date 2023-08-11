"""Bubble Sort is a simple and intuitive sorting algorithm that works by
repeatedly swapping adjacent elements in an array that are out of order until
the entire array is sorted. It starts by comparing the first two elements of
the array, swapping them if necessary, and then moving on to the next pair of
adjacent elements. This process is repeated until all pairs of adjacent
elements have been compared.

Pros: Simple and easy to implement.
Cons: Inefficient for larger datasets and has a time complexity of O(n^2).
Stable: Yes."""

from collections.abc import Callable
from operator import lt, gt
from typing import Optional
from common import SupportsLessThanT


def bubble_sort(sequence: list[SupportsLessThanT],
                key: Optional[Callable[[SupportsLessThanT],
                              SupportsLessThanT]] = None,
				reverse: bool = False) -> None:
	"""In place stable sorting algorithm with O(n^2) time complexity, suitable
	only for small datasets."""

	if reverse:
		compare_operator = lt
	else:
		compare_operator = gt

	n = len(sequence)

	if key:
		keys = [*map(key, sequence)]
	else:
		keys = sequence

	for i in range(n - 1):
		no_swaps = True
		j = n - 1
		
		while j > i:
			if compare_operator(keys[j - 1], keys[j]):
				sequence[j], sequence[j - 1] = sequence[j - 1], sequence[j]
				if key:
					keys[j], keys[j - 1] = keys[j - 1], keys[j]
				no_swaps = False
			j -= 1

		if no_swaps:
			break
