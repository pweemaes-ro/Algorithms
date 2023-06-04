"""In place merge sort based on 'Introduction to Algorithms'. """
from collections.abc import MutableSequence
from operator import lt, gt
from random import randint

from common import SupportsLessThanT


def merge(sequence: MutableSequence[SupportsLessThanT],
          start: int,
          middle: int,
          stop: int,
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
	
	_sorted = []
	inversions = 0
	
	while left < middle and right < stop:
		if operator(sequence[right], sequence[left]):
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
                reverse: bool) -> int:
	inversions = 0
	
	if stop is None:
		stop = len(sequence)
	
	# sequences of 1 or 0 items are already sorted.
	if stop - start <= 1:
		return 0
	
	middle = (stop + start) // 2
	
	inversions += _merge_sort(sequence, start, middle, reverse)
	inversions += _merge_sort(sequence, middle, stop, reverse)
	
	inversions += merge(sequence, start, middle, stop, reverse)
	return inversions


def merge_sort(sequence: MutableSequence[SupportsLessThanT],
               reverse: bool = False) -> int:
	"""The IN PLACE merge sort based upon 'Introduction to Algorithms'. THIS
	algorithm now returns the nr of inversions in the sequence."""

	return _merge_sort(sequence, 0, len(sequence), reverse)


def test_merge_sort() -> None:
	"""Test the merge sort algorithm"""
	
	for i in range(500):
		base_lst = [randint(-i, i) for _ in range(i)]
		for reverse in (False, True):
			lst = list(base_lst)
			sorted_lst = sorted(lst, reverse=reverse)
			merge_sort(lst, reverse)
			assert sorted_lst == lst


def _test_merge_sort() -> None:
	test_merge_sort()
	print("merge_sort_test completed without errors.")

	
if __name__ == "__main__":
	
	def _main() -> None:
		"""Some testing"""
		_test_merge_sort()

	_main()
