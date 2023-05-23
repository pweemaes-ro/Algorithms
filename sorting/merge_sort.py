"""In place merge sort based on 'Introduction to Algorithms'. """
from collections.abc import MutableSequence
from random import shuffle
from typing import Optional

from common import SupportsLessThanT


def _merge(sequence: MutableSequence[SupportsLessThanT],
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

	inversions += _merge(sequence, start, middle, stop)
	return inversions

# The test is "if start >= stop - 1" rather than “if start ≠ stop - 1.” If
# merge_sort is called with start > stop - 1, then the subarray A[p : r] is
# empty. Argue that as long as the initial call of merge_sort(A, 0, n) has
# n ≥ 1, the test “if start != stop - 1” suffices to ensure that no recursive
# call has start > stop - 1.


def test_merge_sort() -> None:
	"""Test the merge sort ('Introduction to Algorithm' version)."""
	
	for i in range(10):
		lst = list(range(i))
		shuffle(lst)
		sorted_lst = sorted(lst)
		merge_sort(lst)
		assert sorted_lst == lst

	# print("merge_sort_test completed without errors.")

	
if __name__ == "__main__":
	
	def _main() -> None:
		"""Some testing"""
		test_merge_sort()

	_main()
	