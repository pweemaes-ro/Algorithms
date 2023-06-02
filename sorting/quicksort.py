"""Quicksort"""
from collections.abc import Sequence, MutableSequence
from random import randint
from typing import TypeAlias, Callable

from common import SupportsLessThanT, SupportsLessThanOrEqualT
from tools import is_sorted

PartitionFunction: TypeAlias = \
	Callable[[MutableSequence[SupportsLessThanOrEqualT], int, int], int]


def _partition_hoare(sequence: MutableSequence[SupportsLessThanOrEqualT],
                     low: int,
                     high: int) -> int:
	"""In place partition the sequence, using te item in the middle as pivot.
	Return the pivot index."""
	
	pivot = sequence[low]
	
	left = low
	right = high

	while True:
		# Find leftmost element greater than or equal to pivot
		while sequence[left] < pivot:
			left += 1
		
		# Find rightmost element smaller than or equal to pivot
		while sequence[right] > pivot:
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
                      high: int) -> int:
	"""In place partition the sequence using the item at the last position as
	pivot. Return the pivot index."""
	
	pivot = sequence[high]  # last item is the pivot
	pivot_idx = low         # destination for swapping items <= pivot to.
	
	for j in range(low, high):
		# items that go in the higher (right) part need no processing since at
		# the end we put the pivot after the last item in the lower (left)
		# part, thereby putting items > pivot in the higher (right) part.
		if sequence[j] <= pivot:
			sequence[pivot_idx], sequence[j] = sequence[j], sequence[pivot_idx]
			pivot_idx += 1
	
	# Swap the pivot to its destination.
	sequence[pivot_idx], sequence[high] = sequence[high], sequence[pivot_idx]

	return pivot_idx


def quicksort_lomuto(sequence: MutableSequence[SupportsLessThanOrEqualT]) \
	-> None:
	"""In place sorting using quicksort algorithm and Lomuto's partitioning
	algorithm."""
	
	_quicksort_lomuto(sequence, 0, len(sequence) - 1)
	

def _quicksort_lomuto(sequence: MutableSequence[SupportsLessThanOrEqualT],
                     low: int,
                     high: int) -> None:

	if low >= high:
		return
	
	p = _partition_lomuto(sequence, low, high)

	_quicksort_lomuto(sequence, low, p - 1)
	_quicksort_lomuto(sequence, p + 1, high)


def quicksort_hoare(sequence: MutableSequence[SupportsLessThanOrEqualT]) \
	-> None:
	"""In place sorting using quicksort algorithm and Hoare's partitioning
	algorithm."""

	_quicksort_hoare(sequence, 0, len(sequence) - 1)


def _quicksort_hoare(sequence: MutableSequence[SupportsLessThanOrEqualT],
                    low: int,
                    high: int) -> None:
	
	if low >= high:
		return
	
	p = _partition_hoare(sequence, low, high)
	
	_quicksort_hoare(sequence, low, p)   # Notice that pivot pos is now included!
	_quicksort_hoare(sequence, p + 1, high)


def quicksort(sequence: Sequence[SupportsLessThanT]) -> list[SupportsLessThanT]:
	"""Return a sorted list with the items of sequence (ergo: NOT in place)."""
	
	if len(sequence) <= 1:
		return list(sequence)

	pivot = sequence[randint(0, len(sequence) - 1)]
	
	smaller, higher, equal = [], [], []
	for item in sequence:
		if item == pivot:
			equal.append(item)
		elif item < pivot:
			smaller.append(item)
		else:
			higher.append(item)
	
	return quicksort(smaller) + equal + quicksort(higher)


def test_quicksort() -> None:
	"""Test all quicksort variants (in place and not in place)."""
	
	for i in range(100):
		lst = [randint(-i, i) for _ in range(i)]
		
		for qs_in_place_func in (quicksort_hoare, quicksort_lomuto):
			unsorted = list(lst)
			qs_in_place_func(unsorted)
			assert is_sorted(unsorted)
			
		for qs_not_in_place_func in (quicksort,):
			sorted_list = qs_not_in_place_func(list(lst))
			assert is_sorted(sorted_list)


if __name__ == "__main__":
	def _main() -> None:
		test_quicksort()
