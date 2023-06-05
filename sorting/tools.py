"""Some generic tools related to sorting."""

import operator
from collections.abc import Sequence, MutableSequence
from copy import copy
from itertools import pairwise
from operator import lt, gt
from random import shuffle, randint
from typing import cast

from common import SupportsLessThanT
from merge_sort import merge_sort


def is_sorted(sequence: Sequence[SupportsLessThanT],
              reverse: bool = False) -> bool:
	"""Return True if sequence is sorted, else False."""
	
	# Todo: Needs optional key function

	if reverse:
		compare_operator = operator.ge
	else:
		compare_operator = operator.le
	
	return all(compare_operator(a, b)
	           for (a, b) in pairwise(sequence))


def inversion_count(sequence: Sequence[SupportsLessThanT],
                    reverse: bool = False) -> int:
	"""Counts the nr of inversions in the sequence. A pair (i, j) is an
	inversion if i < j and sequence[i] > sequence[j]. Notice that the merge
	function checks for inversions (if sequence[left] < sequence[right]), so we
	can use merge_sort to count the nr of inversions recursively! For this to
	work the sequence has to be merge-sorted, so we use a copy of sequence."""
	
	# Todo: Needs (really?) optional key function

	copy_of_sequence: MutableSequence[SupportsLessThanT] = \
		cast(MutableSequence[SupportsLessThanT], copy(sequence))
	
	return merge_sort(copy_of_sequence, reverse=reverse)


def _naive_inversion_count(sequence: Sequence[SupportsLessThanT],
                           reverse: bool = True) -> int:
	"""Only here for comparing with the MUCH faster inversion_count function.
	Only suitable for relatively small sequences, time complexity = O(n^2)."""
	
	inversions = 0
	
	if reverse:
		compare_operator = lt
	else:
		compare_operator = gt
		
	for i in range(len(sequence) - 1):
		left = sequence[i]
		for right in sequence[i + 1:]:
			if compare_operator(left, right):
				inversions += 1
	
	return inversions


def test_is_sorted() -> None:
	for i in range(10, 100):
		lst = list(range(i))
		shuffle(lst)
		
		assert is_sorted(lst) == (lst == sorted(lst))
		assert is_sorted(sorted(lst))
		assert not is_sorted(sorted(lst), reverse=True)
		assert is_sorted(sorted(lst, reverse=True), reverse=True)
		assert not is_sorted(sorted(lst, reverse=True))


def test_inversion_count() -> None:
	"""Test inversion count"""
	
	for i in range(100):
		for reverse in (False, True):
			lst = [randint(-i, i) for _ in range(i)]
			naive_count = _naive_inversion_count(lst, reverse)
			normal_count = inversion_count(lst, reverse)
			assert naive_count == normal_count
	

if __name__ == "__main__":
	def _main() -> None:
		"""Some basic tests"""
		test_inversion_count()
		test_is_sorted()
		
	_main()
