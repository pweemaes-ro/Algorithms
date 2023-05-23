"""Some generic tools related to sorting."""

import operator
from collections.abc import Sequence, MutableSequence
from copy import copy
from itertools import pairwise
from random import shuffle
from typing import cast

from common import SupportsLessThanT
from merge_sort import merge_sort


def is_sorted(sequence: Sequence[SupportsLessThanT],
              ascending: bool = True) -> bool:
	"""Return True if sequence is sorted (ascending), else False."""
	
	if ascending:
		compare_operator = operator.le
	else:
		compare_operator = operator.ge
	
	return all(compare_operator(a, b)
	           for (a, b) in pairwise(sequence))


def inversion_count(sequence: Sequence[SupportsLessThanT]) -> int:
	"""Counts the nr of inversions in the sequence. A pair (i, j) is an
	inversion if i < j and sequence[i] > sequence[j]. Notice that the merge
	function checks for inversions (if sequence[left] < sequence[right]), so we
	can use merge_sort to count the nr of inversions recursively! For this to
	work the sequence has to be merge-sorted, so we use a copy of sequence."""
	
	copy_of_sequence: MutableSequence[SupportsLessThanT] = \
		cast(MutableSequence[SupportsLessThanT], copy(sequence))
	
	return merge_sort(copy_of_sequence)


def _naive_inversion_count(sequence: Sequence[SupportsLessThanT]) -> int:
	"""Only here for comparing with the MUCH faster inversion_count function.
	Only suitable for relatively small sequences, time complexity = O(n^2)."""
	
	inversions = 0
	
	for i in range(len(sequence) - 1):
		left = sequence[i]
		for right in sequence[i + 1:]:
			if left > right:
				inversions += 1
	
	return inversions


def test_is_sorted() -> None:
	for i in range(10, 100):
		lst = list(range(i))
		shuffle(lst)
		
		assert is_sorted(lst) == (lst == sorted(lst))
		assert is_sorted(sorted(lst))
		assert not is_sorted(sorted(lst), ascending=False)
		assert is_sorted(sorted(lst, reverse=True), ascending=False)
		assert not is_sorted(sorted(lst, reverse=True))
		
	# print("is_sorted_test completed without errors.")

def test_inversion_count() -> None:
	"""Test inversion count"""
	
	for i in range(100):
		lst = list(range(i))
		c = inversion_count(lst)
		shuffle(lst)
		naive_count = _naive_inversion_count(lst)
		normal_count = inversion_count(lst)
		assert naive_count == normal_count

		lst = list(reversed(range(i)))
		naive_count = _naive_inversion_count(lst)
		normal_count = inversion_count(lst)
		assert naive_count == normal_count == \
		       (len(lst) * (len(lst) - 1)) // 2
	
	lst = 2 * list(range(10))
	shuffle(lst)
	verify_lst = copy(lst)
	c_1 = inversion_count(lst)
	assert lst == verify_lst    # inversion count should leave lst unchanged
	c_2 = _naive_inversion_count(lst)
	assert lst == verify_lst
	assert c_1 == c_2
	
	# print("inversion_count_test completed without errors.")

if __name__ == "__main__":

	def _main() -> None:
		"""Some basic tests"""
		test_inversion_count()
		test_is_sorted()
		
	_main()
