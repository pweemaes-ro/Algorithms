"""Another sorting algorithm..."""
from collections.abc import MutableSequence
from random import shuffle

from common import SupportsLessThanT


def selection_sort(unsorted: MutableSequence[SupportsLessThanT]) -> None:
	"""In place sorting algorithm. Not very efficient, use merge sort!"""
	
	n = len(unsorted)
	for i in range(n - 1):
		s = i
		for j in range(i + 1, n):
			if unsorted[j] < unsorted[s]:
				s = j
		if s != i:
			unsorted[s], unsorted[i] = unsorted[i], unsorted[s]


if __name__ == "__main__":
 
	def _selection_sort_test() -> None:
		"""Basic tests..."""
		
		for i in range(10):
			lst = list(range(i))
			shuffle(lst)
			py_sorted = sorted(lst)
			selection_sort(lst)
			assert lst == py_sorted
		
		print(f"selection_sort test completed without errors.")
	
	def main() -> None:
		_selection_sort_test()

	main()
