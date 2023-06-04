"""Another sorting algorithm..."""
from collections.abc import MutableSequence
from operator import gt, lt
from random import randint

from common import SupportsLessThanT
from tools import is_sorted


def selection_sort(unsorted: MutableSequence[SupportsLessThanT],
                   reverse: bool = False) -> None:
	"""In place sorting algorithm. Not very efficient, use merge sort!"""
	
	n = len(unsorted)
	
	if reverse:
		compare_operator = gt
	else:
		compare_operator = lt
		
	for i in range(n - 1):
		s = i
		for j in range(i + 1, n):
			if compare_operator(unsorted[j], unsorted[s]):
				s = j
		unsorted[s], unsorted[i] = unsorted[i], unsorted[s]


def test_selection_sort() -> None:
	"""Basic tests..."""
	
	for i in range(100):
		base_list = [randint(-i, i) for _ in range(i)]
		for reverse in (False, True):
			lst = list(base_list)
			selection_sort(lst, reverse)
			assert is_sorted(lst, reverse)
	

if __name__ == "__main__":
	
	def _main() -> None:
		test_selection_sort()

	_main()
