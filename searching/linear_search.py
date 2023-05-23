"""Linear search algorithm,"""
from collections.abc import Sequence
from random import shuffle
from typing import Optional, TypeVar

from common import SupportsLessThanT


def linear_search(data: Sequence[SupportsLessThanT],
                  target: SupportsLessThanT) -> Optional[int]:
	"""Return the 0-based index of *target* in *data* if *target* found in
	*data*, else return *None*"""
	
	for i in range(len(data)):
		if data[i] == target:
			return i
	
	return None


T = TypeVar("T")

items_tested = 0


def _linear_search(sequence: Sequence[T], n: int, key: T) -> Optional[int]:
	"""Return the index of the first occurance of x, or None if not found.
	This implementation only for the sake of answering the questions (and
	verifying the answers with functions)."""
	
	global items_tested
	i = 0
	
	while i < n:
		items_tested += 1
		if sequence[i] == key:  # Checks: average = (n + 1) / 2, worst case = n.
			return i
		i += 1
	
	return None


# QUESTIONS about _linear_search:
#
# 1. How many elements of *sequence* need to be checked on average, assuming
#    that the key is equailly likely to be any element in *sequence*?
#
# 2. How about the worst case?
#
# 3. Using Theta notation, give the average case and worst case runtimes.
#
# JUSTIFY YOUR ANSWERS!
#
# ANSWERS:
#
# 1. If the key is the first item, 1 item is checked.
#    If the key is the second item, 2 items are checked.
#    ...
#    If the key is the last item (or not found), n items are checked.
#    Since each is equally likely, we have that the average nr of items checked
#    is sum(1 to n) / n = ((n * (n + 1)) / 2) / n = (n + 1) / 2.
#    THIS IS VERIFIED BY average_case() function below.
#
# 2. Worst case is when the key is NOT in the sequence. Then all n items are
#    checked.
#    THIS IS VERIFIED BY worst_case() function below.
#
# 3. Both average and worst case are O(n). This follows from the fact that the
#    nr of times the item test is executed is linear in both cases. This test
#    is the only dependency on n.
#
# Notice that in the best case, the first item is the key, and then the test
# is executed exactly 1 time, so best case is constant time O(1).


if __name__ == "__main__":
	
	def _linear_search_test() -> None:
		"""Test binary_search function."""
		
		# search_func = linear_search
		for i in range(10):
			data = list(range(i))
			for target in data:
				assert linear_search(data, target) == target
			
			assert linear_search([], 1) is None
			assert linear_search([], 0) is None
			
			not_in_data = (-1, i)
			for target in not_in_data:
				assert linear_search(data, target) is None

		print("linear_search_test completed without errors.")
	
	
	def _average_case() -> None:
		"""Tests assumption that on average the nr of checks in linear search
		algorithm is (n + 1) / 2."""
		
		global items_tested
		
		items_tested = 0
		nr_tests = 500000
		n = 10
		
		for i in range(nr_tests):
			lst = list(range(n))
			shuffle(lst)
			_linear_search(lst, n, 0)
		
		assert f"{(n + 1) / 2:.2f}" == f"{items_tested / nr_tests:.2f}"
	
	
	def _worst_case() -> None:
		"""Tests assumption that in the worst case the nr of checks in linear
		search algorithm is n."""
		
		global items_tested
		items_tested = 0
		nr_tests = 500000
		n = 10
		
		for i in range(nr_tests):
			lst = list(range(n))
			shuffle(lst)
			_linear_search(lst, n, -1)
		
		assert f"{n:.2f}" == f"{items_tested / nr_tests:.2f}"
	
	def main() -> None:
		"""Do some basic tests..."""
		_linear_search_test()
		# _average_case()
		# _worst_case()

	main()
