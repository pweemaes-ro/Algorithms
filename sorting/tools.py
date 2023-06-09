"""Some generic tools related to sorting."""

import operator
from collections.abc import Sequence, MutableSequence, Callable
from copy import copy
from itertools import pairwise
from operator import lt, gt
from typing import cast, Optional

from common import SupportsLessThanT
from merge_sort import merge_sort


def is_sorted(sequence: Sequence[SupportsLessThanT],
              key: Optional[Callable[[SupportsLessThanT],
                            SupportsLessThanT]] = None,
              reverse: bool = False) -> bool:
	"""Return True if sequence is sorted, else False."""

	if reverse:
		compare_operator = operator.ge
	else:
		compare_operator = operator.le

	if key:
		keys: Sequence[SupportsLessThanT] = [*map(key, sequence)]
	else:
		keys = sequence
		
	return all(compare_operator(a, b) for (a, b) in pairwise(keys))


def inversion_count(sequence: Sequence[SupportsLessThanT],
                    reverse: bool = False) -> int:
	"""Counts the nr of inversions in the sequence. A pair (i, j) is an
	inversion if i < j and sequence[i] > sequence[j]. Notice that the merge
	function checks for inversions (if sequence[left] < sequence[right]), so we
	can use merge_sort to count the nr of inversions recursively! For this to
	work the sequence has to be merge-sorted, so we use a copy of sequence."""

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
