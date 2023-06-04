"""Quicksort"""
from collections.abc import Sequence, MutableSequence
from operator import lt, gt, ge, le
from random import randint
from typing import TypeAlias, Callable

from common import SupportsLessThanT, SupportsLessThanOrEqualT
from tools import is_sorted

PartitionFunction: TypeAlias = \
	Callable[[MutableSequence[SupportsLessThanOrEqualT], int, int], int]


def _partition_hoare(sequence: MutableSequence[SupportsLessThanOrEqualT],
                     low: int,
                     high: int,
                     reverse: bool = False) -> int:
	"""In place partition the sequence, using te item in the middle as pivot.
	Return the pivot index."""
	
	pivot = sequence[low]
	
	left = low
	right = high
	
	if reverse:
		left_before_pivot = gt
		right_before_pivot = lt
	else:
		left_before_pivot = lt
		right_before_pivot = gt
		
	while True:
		# Find leftmost element greater than or equal to pivot
		# while sequence[left] < pivot:
		while left_before_pivot(sequence[left], pivot):
			left += 1
		
		# Find rightmost element smaller than or equal to pivot
		# while sequence[right] > pivot:
		while right_before_pivot(sequence[right], pivot):
			right -= 1
	
		# If two pointers met...
		if left >= right:
			return right
		
		sequence[left], sequence[right] = sequence[right], sequence[left]
		# Move both pointers to the next item
		left += 1
		right -= 1


def _partition_lomuto(sequence: MutableSequence[SupportsLessThanOrEqualT],
                      low: int,
                      high: int,
                      reverse: bool = False) -> int:
	"""In place partition the sequence using the item at the last position as
	pivot. Return the pivot index."""
	
	pivot = sequence[high]  # last item is the pivot
	pivot_idx = low         # destination for swapping items <= pivot to.
	
	if reverse:
		compare_operator = ge
	else:
		compare_operator = le
		
	for j in range(low, high):
		# items that go in the higher (right) part need no processing since at
		# the end we put the pivot after the last item in the lower (left)
		# part, thereby putting items > pivot in the higher (right) part.
		# if sequence[j] <= pivot:
		if compare_operator(sequence[j], pivot):
			sequence[pivot_idx], sequence[j] = sequence[j], sequence[pivot_idx]
			pivot_idx += 1
	
	# Swap the pivot to its destination.
	sequence[pivot_idx], sequence[high] = sequence[high], sequence[pivot_idx]

	return pivot_idx


def quicksort_lomuto(sequence: MutableSequence[SupportsLessThanOrEqualT],
                     reverse: bool = False) -> None:
	"""In place sorting using quicksort algorithm and Lomuto's partitioning
	algorithm."""
	
	_quicksort_lomuto(sequence, 0, len(sequence) - 1, reverse)
	

def _quicksort_lomuto(sequence: MutableSequence[SupportsLessThanOrEqualT],
                      low: int,
                      high: int,
                      reverse: bool = False) -> None:

	if low >= high:
		return
	
	p = _partition_lomuto(sequence, low, high, reverse)

	_quicksort_lomuto(sequence, low, p - 1, reverse)
	_quicksort_lomuto(sequence, p + 1, high, reverse)


def quicksort_hoare(sequence: MutableSequence[SupportsLessThanOrEqualT],
                    reverse: bool = False) \
	-> None:
	"""In place sorting using quicksort algorithm and Hoare's partitioning
	algorithm."""

	_quicksort_hoare(sequence, 0, len(sequence) - 1, reverse)


def _quicksort_hoare(sequence: MutableSequence[SupportsLessThanOrEqualT],
                     low: int,
                     high: int,
                     reverse: bool = False) -> None:
	
	if low >= high:
		return
	
	p = _partition_hoare(sequence, low, high, reverse)
	
	_quicksort_hoare(sequence, low, p, reverse)         # pivot pos  included!
	_quicksort_hoare(sequence, p + 1, high, reverse)


def quicksort(sequence: Sequence[SupportsLessThanT],
              reverse: bool = False) -> list[SupportsLessThanT]:
	"""Return a sorted list with the items of sequence (ergo: NOT in place)."""
	
	if len(sequence) <= 1:
		return list(sequence)

	if reverse:
		smaller_operator = gt
	else:
		smaller_operator = lt
	
	pivot = sequence[randint(0, len(sequence) - 1)]
	
	smaller, higher, equal = [], [], []
	for item in sequence:
		if item == pivot:
			equal.append(item)
		elif smaller_operator(item, pivot):
			smaller.append(item)
		else:
			higher.append(item)
	
	return quicksort(smaller, reverse) + equal + quicksort(higher, reverse)


def test_quicksort() -> None:
	"""Test all quicksort variants (in place and not in place)."""
	
	for i in range(500):
		base_lst = [randint(-i, i) for _ in range(i)]
		
		for qs_in_place_func in (quicksort_hoare, quicksort_lomuto):
			for reverse in (False, True):
				lst = list(base_lst)
				qs_in_place_func(lst, reverse=reverse)
				assert is_sorted(lst, reverse)

		for qs_not_in_place_func in (quicksort,):
			for reverse in (False, True):
				lst = list(base_lst)
				sorted_list = qs_not_in_place_func(lst, reverse)
				assert is_sorted(sorted_list, reverse)
				print(sorted_list)


if __name__ == "__main__":
	def _main() -> None:
		test_quicksort()
