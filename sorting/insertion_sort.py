"""Not suitable for large sequences..."""
from collections.abc import Callable
from operator import lt, gt
from typing import MutableSequence, Optional

from common import SupportsLessThanT


def insertion_sort_recursive(sequence: list[SupportsLessThanT],
                             key: Optional[Callable[[SupportsLessThanT],
                                           SupportsLessThanT]] = None,
                             reverse: bool = False) -> None:
	"""You can also think of insertion sort as a recursive algorithm. In order
	to sort A[0: n], recursively sort the subarray A[0: n – 1] and then
	insert A[n] into the sorted subarray A[0 : n – 1]."""

	if reverse:
		compare_func = gt
	else:
		compare_func = lt

	if key:
		keys = [*map(key, sequence)]
	else:
		keys = sequence

	def _insertion_sort_recursive(_sequence: MutableSequence[SupportsLessThanT],
	                              n: int) -> None:
		n -= 1
		if n < 1:
			return
		
		_insertion_sort_recursive(_sequence, n)
		_move_to_place(_sequence, n, compare_func, 0, len(sequence), keys)
	
	_insertion_sort_recursive(sequence, len(sequence))


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

	while stop > j >= start + 1 and compare_func(key, keys[j - 1]):
		sequence[j] = sequence[j - 1]
		if keys is not sequence:
			keys[j] = keys[j - 1]
		j -= 1
	
	sequence[j] = key_item
	if keys is not sequence:
		keys[j] = key


def insertion_sort(sequence: list[SupportsLessThanT],
                   start: int = 0,
                   stop: Optional[int] = None,
                   key: Optional[Callable[[SupportsLessThanT],
                                          SupportsLessThanT]] = None,
                   reverse: bool = False) -> None:
	"""New version that supports sorting from start to stop locations."""
	
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
	"""New version that supports sorting from start to stop locations."""
	
	if stop is None:
		stop = len(sequence)

	if reverse:
		compare_func = gt
	else:
		compare_func = lt

	for i in range(start, stop):
		_move_to_place(sequence, i, compare_func, start, stop, keys)
