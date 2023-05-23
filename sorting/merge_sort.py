"""In place merge sort based on 'Introduction to Algorithms'. """
from collections.abc import MutableSequence, Sequence
from copy import copy
from random import shuffle
from typing import Optional, cast

from common import SupportsLessThanT


def naive_inversion_count(sequence: Sequence[SupportsLessThanT]) -> int:
	"""Only here for comparing with the MUCH faster inversion_count function.
	Only suitable for relatively small sequences, time complexity = O(n^2)."""
	
	inversions = 0
	
	for i in range(len(sequence) - 1):
		left = sequence[i]
		for right in sequence[i+1:]:
			if left > right:
				inversions += 1

	return inversions


def merge_ita2(sequence: MutableSequence[SupportsLessThanT],
              start: int,
              middle: int,
              stop: int) -> int:
	"""In place merge based on 'Introduction to Algorithms' Returns the nr of
	inversions detected."""

	# Instead of directly copying data to sequence (see merge_ita) we create a
	# new sorted list, which we put in the unsorted sequence when all data is
	# in sorted list.

	left = start
	right = middle

	_sorted = []
	inversions = 0
	while left < middle and right < stop:
		if sequence[right] < sequence[left]:
			inversions += middle - left
			_sorted.append(sequence[right])
			right += 1
		else:
			_sorted.append(sequence[left])
			left += 1

	_sorted.extend(sequence[left:middle])
	_sorted.extend(sequence[right:stop])

	sequence[start:stop] = _sorted
	
	return inversions


def merge_sort(sequence: MutableSequence[SupportsLessThanT],
               start: int = 0,
               stop: Optional[int] = None) -> int:
	"""The IN PLACE merge sort based upon 'Introduction to Algorithms'. THIS
	algorithm now returns the nr of inversions in the sequence."""
	
	inversions = 0
	
	if stop is None:
		stop = len(sequence)
	
	# sequences of 1 or 0 items are sorted already!
	if stop - start <= 1:
		return 0
	
	middle = (stop + start) // 2
	
	inversions += merge_sort(sequence, start, middle)
	inversions += merge_sort(sequence, middle, stop)

	inversions += merge_ita2(sequence, start, middle, stop)
	return inversions


def inversion_count(sequence: Sequence[SupportsLessThanT]) -> int:
	"""Counts the nr of inversions in the sequence. A pair (i, j) is an
	inversion if i < j and sequence[i] > sequence[j]. Notice that the merge
	function checks for inversions (if sequence[left] < sequence[right]), so we
	can use merge_sort to count the nr of inversions recursively! For this to
	work the sequence has to be merge-sorted, so we use a copy of sequence."""
	
	copy_of_sequence: MutableSequence[SupportsLessThanT] = \
		cast(MutableSequence[SupportsLessThanT], copy(sequence))
	
	return merge_sort(copy_of_sequence)


if __name__ == "__main__":

	def merge_sort_test() -> None:
		"""Test the merge sort ('Introduction to Algorithm' version)."""
		
		for i in range(10):
			lst = list(range(i))
			shuffle(lst)
			sorted_lst = sorted(lst)
			merge_sort(lst)
			assert sorted_lst == lst
	

	def inversion_count_test() -> None:
		"""Test inversion count"""

		for i in range(100):
			
			lst = list(range(i))
			c = inversion_count(lst)
			assert c == 0
			assert c == naive_inversion_count(lst)
			
			lst = list(reversed(range(i)))
			c = inversion_count(lst)
			assert c == (len(lst) * (len(lst) - 1)) // 2
			assert c == naive_inversion_count(lst)
		
		lst = 2 * list(range(10))
		shuffle(lst)
		verify_lst = copy(lst)
		c_1 = inversion_count(lst)
		assert lst == verify_lst
		c_2 = naive_inversion_count(lst)
		assert lst == verify_lst
		assert c_1 == c_2
	
	
	merge_sort_test()
	inversion_count_test()
