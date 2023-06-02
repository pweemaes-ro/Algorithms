"""Yet another sorting algorithm..."""
from operator import lt, gt
from collections.abc import MutableSequence

from common import SupportsLessThanT


# def bubble_sort_rp(array):
#
# 	n = len(array)
#
# 	for i in range(n - 1):
# 		# Create a flag that will allow the function to
# 		# terminate early if there's nothing left to sort
# 		already_sorted = True
#
# 		# Start looking at each item of the list one by one,
# 		# comparing it with its adjacent value. With each
# 		# iteration, the portion of the array that you look at
# 		# shrinks because the remaining items have already been
# 		# sorted.
#
# 		for j in range(n - i - 1):
# 			if array[j] > array[j + 1]:
# 				# If the item you're looking at is greater than its
# 				# adjacent value, then swap them
# 				array[j], array[j + 1] = array[j + 1], array[j]
#
# 				# Since you had to swap two elements,
# 				# set the `already_sorted` flag to `False` so the
# 				# algorithm doesn't finish prematurely
# 				already_sorted = False
#
# 		# If there were no swaps during the last iteration,
# 		# the array is already sorted, and you can terminate
# 		if already_sorted:
# 			break
#
# 	# return array

def bubble_sort(sequence: MutableSequence[SupportsLessThanT],
				reverse: bool = False) -> None:
	"""Inefficient but 'popular'... """

	if reverse:
		compare_operator = gt
	else:
		compare_operator = lt

	n = len(sequence)

	for i in range(n - 1):
		
		no_swaps = True

		j = n - 1
		
		while j > i:
			if compare_operator(sequence[j], sequence[j - 1]):
				sequence[j], sequence[j - 1] = sequence[j - 1], sequence[j]
				no_swaps = False
			j -= 1

		if no_swaps:
			break


def test_bubble_sort() -> None:
	"""Test the merge sort ('Introduction to Algorithm' version)."""
	
	from random import randint
	
	for i in range(100):
		lst = [randint(-1, i) for _ in range(i)]
		sorted_lst = sorted(lst)
		bubble_sort(lst)
		assert sorted_lst == lst


if __name__ == "__main__":
	def _main() -> None:
		"""Some testing"""
		test_bubble_sort()
		
	_main()
