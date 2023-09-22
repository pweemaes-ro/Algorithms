"""Quicksort"""
from collections.abc import Sequence, MutableSequence
from operator import lt, gt, ge, le
from random import randint
from typing import Callable, Optional

from common import SupportsLessThanT


def _set_median_key(sequence: MutableSequence[SupportsLessThanT],
                    low: int,
                    high: int,
                    keys: MutableSequence[SupportsLessThanT],
                    destination: int) -> None:

	if high - low < 10:  # no point in wasting time for small sequence
		return
	
	middle = (low + high) // 2
	median_value = sorted([sequence[low],
	                       sequence[high],
	                       sequence[middle]])[1]
	
	if sequence[low] == median_value:
		median_index = low
	elif sequence[high] == median_value:
		median_index = high
	else:
		median_index = middle

	if destination == median_index:
		return
	
	sequence[destination], sequence[median_index] = \
		sequence[median_index], sequence[destination]
	if keys is not sequence:
		keys[destination], keys[median_index] = \
			keys[median_index], keys[destination]


def _partition_lomuto(sequence: MutableSequence[SupportsLessThanT],
                      low: int,
                      high: int,
                      keys: MutableSequence[SupportsLessThanT],
                      reverse: bool = False) -> int:
	"""In place partition the sequence using the item at the last position as
	pivot. Return the pivot index."""
	
	_set_median_key(sequence, low, high, keys, high)
	
	# last item in (sub)array is the pivot:
	pivot_key = keys[high]
	
	# destination for swapping items <= pivot to, moves one position to the
	# right after each swap:
	pivot_idx = low
	
	if reverse:
		compare_operator = ge
	else:
		compare_operator = le
		
	for j in range(low, high):
		# items that go in the higher (right) part need no processing since at
		# the end we put the pivot after the last item in the lower (left)
		# part, thereby putting items > pivot in the higher (right) part.
		if compare_operator(keys[j], pivot_key):
			if keys is not sequence:
				keys[pivot_idx], keys[j] = keys[j], keys[pivot_idx]
			sequence[pivot_idx], sequence[j] = sequence[j], sequence[pivot_idx]
			pivot_idx += 1
	
	# Swap the pivot to its destination.
	if keys is not sequence:
		keys[pivot_idx], keys[high] = keys[high], keys[pivot_idx]
	sequence[pivot_idx], sequence[high] = sequence[high], sequence[pivot_idx]

	return pivot_idx


def _quicksort_lomuto(sequence: MutableSequence[SupportsLessThanT],
                      low: int,
                      high: int,
                      keys: MutableSequence[SupportsLessThanT],
                      reverse: bool = False) -> None:
	if low >= high:
		return
	
	p = _partition_lomuto(sequence, low, high, keys, reverse)
	
	_quicksort_lomuto(sequence, low, p - 1, keys, reverse)
	_quicksort_lomuto(sequence, p + 1, high, keys, reverse)


def quicksort_lomuto(sequence: list[SupportsLessThanT],
                     key: Optional[Callable[[SupportsLessThanT],
                                   SupportsLessThanT]] = None,
                     reverse: bool = False) -> None:
	"""In place sorting using quicksort algorithm and Lomuto's partitioning
	algorithm."""

	if key:
		keys = [*map(key, sequence)]
	else:
		keys = sequence
	
	_quicksort_lomuto(sequence, 0, len(sequence) - 1, keys, reverse)


def _partition_hoare(sequence: MutableSequence[SupportsLessThanT],
                     low: int,
                     high: int,
                     keys: MutableSequence[SupportsLessThanT],
                     reverse: bool = False) -> int:
	"""In place partition the sequence, using te item in the first position as
	pivot. Return the pivot index. Notice that this differs from the Lomuto
	partitioning in the choice of the pivot value's location, but also in the
	implementation of the partitioning """

	_set_median_key(sequence, low, high, keys, low)
	pivot_key = keys[low]
	
	left = low
	right = high
	
	if reverse:
		left_before_pivot = gt
		right_before_pivot = lt
	else:
		left_before_pivot = lt
		right_before_pivot = gt
	
	while True:
		# Move inward to right until 'left' points to an element >= pivot (or
		# <= pivot if reversed).
		while left_before_pivot(keys[left], pivot_key):
			left += 1

		# Move inward to left until 'right' points to an element <= to pivot
		# (or >= pivot if reversed).
		while right_before_pivot(keys[right], pivot_key):
			right -= 1
		
		# If 'left' and 'right' met, or crossed, we're done. 'right' now points
		# to a value <= pivot (or >= pivot if reversed)...
		if left >= right:
			return right
		
		# ... else we swap what left points to and what right points to, so
		# after swap element >= pivot at right of pivot and element <= pivot at
		# left of pivot (or the other way around if reversed).
		if keys is not sequence:
			keys[left], keys[right] = keys[right], keys[left]
		sequence[left], sequence[right] = sequence[right], sequence[left]
		
		# Move both pointers 'inward' to the next item ('left' moves one position
		# to the right, 'right' moves one position to the left
		left += 1
		right -= 1


def _quicksort_hoare(sequence: MutableSequence[SupportsLessThanT],
                     low: int,
                     high: int,
                     keys: MutableSequence[SupportsLessThanT],
                     reverse: bool = False) -> None:
	
	if low >= high:
		return

	p = _partition_hoare(sequence, low, high, keys, reverse)
	
	_quicksort_hoare(sequence, low, p, keys, reverse)  # pivot pos included!
	_quicksort_hoare(sequence, p + 1, high, keys, reverse)


def quicksort_hoare(sequence: list[SupportsLessThanT],
                    key: Optional[Callable[[SupportsLessThanT],
                                  SupportsLessThanT]] = None,
                    reverse: bool = False) -> None:
	"""In place sorting using quicksort algorithm and Hoare's partitioning
	algorithm."""

	if key:
		keys = [*map(key, sequence)]
	else:
		keys = sequence

	_quicksort_hoare(sequence, 0, len(sequence) - 1, keys, reverse)


def _quicksort(sequence_and_keys:
				Sequence[tuple[SupportsLessThanT, SupportsLessThanT]],
               reverse: bool) \
	-> list[tuple[SupportsLessThanT, SupportsLessThanT]]:

	if len(sequence_and_keys) <= 1:
		return list(sequence_and_keys)

	if reverse:
		smaller_operator = gt
	else:
		smaller_operator = lt

	pivot_key = sequence_and_keys[randint(0, len(sequence_and_keys) - 1)][1]
	
	smaller, larger, equal = [], [], []
	
	for offset, item_and_key in enumerate(sequence_and_keys):
		key = item_and_key[1]
		if key == pivot_key:
			equal.append(item_and_key)
		elif smaller_operator(key, pivot_key):
			smaller.append(item_and_key)
		else:
			larger.append(item_and_key)

	return _quicksort(smaller, reverse) \
		+ equal \
		+ _quicksort(larger, reverse)


def quicksort(sequence: list[SupportsLessThanT],
              key: Optional[Callable[[SupportsLessThanT],
                            SupportsLessThanT]] = None,
              reverse: bool = False) -> list[SupportsLessThanT]:
	"""Return a sorted list with the items of sequence (ergo: NOT in place)."""
	
	if key:
		keys = [*map(key, sequence)]
	else:
		keys = sequence

	items_and_keys = [(item, key) for (item, key) in zip(sequence, keys)]
	sorted_items_and_keys = _quicksort(items_and_keys, reverse)
	
	return [item_and_key[0] for item_and_key in sorted_items_and_keys]
