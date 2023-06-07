"""Yet another sorting algorithm..."""
from functools import lru_cache
from operator import lt, gt, attrgetter, itemgetter
from collections.abc import MutableSequence, Callable
from typing import Any, Optional

from common import SupportsLessThanT
from key_functions import identity_key


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
                key: Optional[Callable[..., Any]] = None,
				reverse: bool = False) -> None:
	"""Inefficient but 'popular'... And stable. """
	if reverse:
		compare_operator = lt
	else:
		compare_operator = gt

	n = len(sequence)

	key = key or identity_key
	
	for i in range(n - 1):
		
		no_swaps = True

		j = n - 1
		
		while j > i:
			cmp_result = compare_operator(key(sequence[j - 1]),
			                              key(sequence[j]))

			if cmp_result:
				sequence[j], sequence[j - 1] = sequence[j - 1], sequence[j]
				no_swaps = False
			j -= 1

		if no_swaps:
			break


def test_bubble_sort() -> None:
	"""Test the merge sort ('Introduction to Algorithm' version)."""
	
	from random import randint
	
	@lru_cache
	def is_odd(x: int) -> int:
		"""key function to sort by odd/even."""
		return x % 2
	
	class Sortable:
		"""A simple sortable class to test 'attrgetter' key."""
		
		def __init__(self, key_value: int):
			self.key_value = key_value
			self.derived = key_value % 3
		
		def __lt__(self, other: Any) -> bool:
			if isinstance(other, type(self)):
				return self.key_value < other.key_value
			else:
				raise NotImplementedError

		def __repr__(self) -> str:
			return f"({self.key_value}, {self.derived})"
		
	for i in range(100):
		base_lst = [randint(-i, i) for _ in range(i)]
		for reverse in (False, True):
			for key in (None, abs, is_odd):
				lst = list(base_lst)
				bubble_sort(lst, reverse=reverse, key=key)
				# bubble_sort is stable sort!
				assert lst == sorted(lst, reverse=reverse, key=key)

			attrgetter_key = attrgetter('derived')
			attrgetter_list = [Sortable(randint(-i, i)) for _ in range(i)]
			bubble_sort(attrgetter_list, reverse=reverse, key=attrgetter_key)
			# bubble_sort is stable sort!
			assert attrgetter_list == sorted(attrgetter_list,
			                                 reverse=reverse,
			                                 key=attrgetter_key)

			itemgetter_key = itemgetter(1)
			itemgetter_list = [(x := randint(-i, i), x % 3) for _ in range(i)]
			bubble_sort(itemgetter_list, reverse=reverse, key=itemgetter_key)
			# bubble_sort is stable sort!
			assert itemgetter_list == sorted(itemgetter_list,
			                                 reverse=reverse,
			                                 key=itemgetter_key)


if __name__ == "__main__":
	def _main() -> None:
		"""Some testing"""
		test_bubble_sort()
		
	_main()
