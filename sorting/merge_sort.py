"""In place merge sort based on 'Introduction to Algorithms'. """
from collections.abc import MutableSequence, Callable
from operator import lt, gt
from random import randint
from typing import Optional, Any

from common import SupportsLessThanT
from key_functions import identity_key


def merge(sequence: MutableSequence[SupportsLessThanT],
          start: int,
          middle: int,
          stop: int,
          key: Optional[Callable[..., Any]] = None,
          reverse: bool = False) -> int:
	"""In place merge based on 'Introduction to Algorithms' Returns the nr of
	inversions detected."""

	# Instead of directly copying data to sequence (see merge_ita) we create a
	# new sorted list, which we put in the unsorted sequence when all data is
	# in sorted list.

	left = start
	right = middle

	if reverse:
		operator = gt
	else:
		operator = lt
	
	key = key or identity_key

	_sorted = []
	inversions = 0
	
	while left < middle and right < stop:
		if operator(key(sequence[right]), key(sequence[left])):
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


def _merge_sort(sequence: MutableSequence[SupportsLessThanT],
                start: int,
                stop: int,
                key: Callable[..., Any],
                reverse: bool) -> int:
	inversions = 0
	
	if stop is None:
		stop = len(sequence)
	
	# sequences of 1 or 0 items are already sorted.
	if stop - start <= 1:
		return 0
	
	middle = (stop + start) // 2
	
	inversions += _merge_sort(sequence, start, middle, key, reverse)
	inversions += _merge_sort(sequence, middle, stop, key, reverse)
	
	inversions += merge(sequence, start, middle, stop, key, reverse)
	return inversions


def merge_sort(sequence: MutableSequence[SupportsLessThanT],
               key: Optional[Callable[..., Any]] = None,
               reverse: bool = False) -> int:
	"""The IN PLACE merge sort based upon 'Introduction to Algorithms'. THIS
	algorithm now returns the nr of inversions in the sequence."""

	key = key or identity_key

	return _merge_sort(sequence, 0, len(sequence), key=key, reverse=reverse)


def test_merge_sort() -> None:
	"""Test the merge sort algorithm"""
	
	def mod_3(n: int) -> int:
		"""Just a test key function """
		
		return n % 3
	
	for i in range(500):
		base_lst = [randint(-i, i) for _ in range(i)]
		for key in (None, abs, mod_3):
			for reverse in (False, True):
				lst = list(base_lst)
				sorted_lst = sorted(lst, key=key, reverse=reverse)
				merge_sort(lst, key, reverse)
				assert sorted_lst == lst


def _test_merge_sort() -> None:
	test_merge_sort()
	print("merge_sort_test completed without errors.")

	
if __name__ == "__main__":
	
	def _main() -> None:
		"""Some testing"""
		_test_merge_sort()

	_main()
