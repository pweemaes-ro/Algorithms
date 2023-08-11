"""nsertion Sort is a sorting algorithm that works by iteratively building a
sorted subarray at the beginning of an array. Starting with the second element,
it compares the current element with its predecessor and shifts the predecessor
subarray until the current element is in its correct location. This process is
repeated for each element in the array until the entire array is sorted.

Pros: Simple and easy to implement, efficient for small datasets.
Cons: Inefficient for larger datasets and has a time complexity of O(n^2).
Stable: Yes."""
from collections.abc import Callable
from operator import lt, gt
from typing import MutableSequence, Optional

from common import SupportsLessThanT


def insertion_sort_recursive(sequence: list[SupportsLessThanT],
                             start: int = 0,
                             stop: Optional[int] = None,
                             key: Optional[Callable[[SupportsLessThanT],
                                           SupportsLessThanT]] = None,
                             reverse: bool = False) -> None:
	"""In place stable sorting algorithm with O(n^2) time complexity. Suitable
	only for small datasets.
	
	You can also think of insertion sort as a recursive algorithm. In order
	to sort A[0: n], recursively sort the subarray A[0: n – 1] and then
	insert A[n] into the sorted subarray A[0 : n – 1]."""

	if stop is None:
		stop = len(sequence)
	if reverse:
		compare_func = gt
	else:
		compare_func = lt

	if key:
		keys = [*map(key, sequence)]
	else:
		keys = sequence

	def _insertion_sort_recursive(_sequence: MutableSequence[SupportsLessThanT],
	                              n: int,
	                              _start: int,
	                              _stop: int) -> None:
		
		n -= 1
		if n < 1:
			return
		
		_insertion_sort_recursive(_sequence, n, _start, _stop)
		_move_to_place(_sequence, n, compare_func, _start, _stop, keys)
	
	_insertion_sort_recursive(sequence, len(sequence), start, stop)


def _move_to_place(sequence: MutableSequence[SupportsLessThanT],
                   key_index: int,
                   compare_func: Callable[[SupportsLessThanT,
                                          SupportsLessThanT], bool],
                   start: int,
                   stop: int,
                   keys: MutableSequence[SupportsLessThanT]) -> None:
	"""Insert sequence[key_index] into the sorted subarray
	sequence[: key_index]."""

	key_item = sequence[key_index]
	key = keys[key_index]
	j = key_index
	must_swap_keys = keys is not sequence
	
	while stop > j >= start + 1 and compare_func(key, keys[j - 1]):
		sequence[j] = sequence[j - 1]
		if must_swap_keys:
			keys[j] = keys[j - 1]
		j -= 1
	
	sequence[j] = key_item
	if must_swap_keys:
		keys[j] = key


def insertion_sort(sequence: list[SupportsLessThanT],
                   start: int = 0,
                   stop: Optional[int] = None,
                   key: Optional[Callable[[SupportsLessThanT],
                                          SupportsLessThanT]] = None,
                   reverse: bool = False) -> None:
	"""In place stable sorting algorith with O(n^2) time complexity. Suitable
	only for small datasets."""
	
	if stop is None:
		stop = len(sequence)

	if key:
		keys = [*map(key, sequence)]
	else:
		keys = sequence

	_insertion_sort(sequence, start, stop, keys, reverse)


def _insertion_sort(sequence: MutableSequence[SupportsLessThanT],
                   start: int,
                   stop: int,
                   keys: MutableSequence[SupportsLessThanT],
                   reverse: bool = False) -> None:
	"""Internal version that uses key-values (calculated using a key function)
	to avoid recalculating keys more than once per sequence item."""
	
	if reverse:
		compare_func = gt
	else:
		compare_func = lt

	for i in range(start, stop):
		_move_to_place(sequence, i, compare_func, start, stop, keys)
