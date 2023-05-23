"""Not suitable for large sequences..."""
import operator
from collections.abc import Callable
from itertools import pairwise
from random import shuffle
from typing import MutableSequence, Sequence, TypeVar, Optional

from common import SupportsLessThanT


# PSEUDOCODE (adapted for zero-based indexes):
# INSERTION-SORT(sequence, n)
# 1 for i = 1 to n - 1
# 2     key = sequence[i]
# 3     // Insert sequence[i] into the sorted subarray sequence[: i – 1].
# 4     j = i – 1
# 5     while j >= 0 and sequence[j] > key
# 6         sequence[j + 1] = sequence[j]
# 7         j = j – 1
# 8     sequence[j + 1] = key

# At the start of each iteration of the for loop of lines 1–8, the subarray
# sequence[: i – 1] consists of the elements originally in sequence[: i – 1],
# but in sorted order. These properties of sequence[: i - 1] are a loop
# invariant. A property is loop-invariant if:

# Initialization: It is true prior to the first iteration of the loop.
# Maintenance: If it is true before an iteration of the loop, it remains true
#   before the next iteration.
# Termination: The loop terminates, and when it terminates, the invariant
#   — usually along with the reason that the loop terminated — gives us a
#   useful property that helps show that the algorithm is correct.

# Initialization: We start by showing that the loop invariant holds before
# the first loop iteration, when i = 2.2 The subarray A[1 : i – 1] consists
# of just the single element A[1], which is in fact the original element in
# A[1]. Moreover, this subarray is sorted (after all, how could a subarray
# with just one value not be sorted?), which shows that the loop
# invariant holds prior to the first iteration of the loop.
# Maintenance: Next, we tackle the second property: showing that each
# iteration maintains the loop invariant. Informally, the body of the for
# loop works by moving the values in A[i – 1], A[i – 2], A[i – 3], and so
# on by one position to the right until it finds the proper position for
# A[i] (lines 4–7), at which point it inserts the value of A[i] (line 8). The
# subarray A[1 : i] then consists of the elements originally in A[1 : i], but
# in sorted order. Incrementing i (increasing its value by 1) for the next
# iteration of the for loop then preserves the loop invariant.
# A more formal treatment of the second property would require us to
# state and show a loop invariant for the while loop of lines 5–7. Let’s
# not get bogged down in such formalism just yet. Instead, we’ll rely on
# our informal analysis to show that the second property holds for the
# outer loop.
# Termination: Finally, we examine loop termination. The loop variable i
# starts at 2 and increases by 1 in each iteration. Once i’s value exceeds n
# in line 1, the loop terminates. That is, the loop terminates once i
# equals n + 1. Substituting n + 1 for i in the wording of the loop
# invariant yields that the subarray A[1 : n] consists of the elements
# originally in A[1 : n], but in sorted order. Hence, the algorithm is
# correct.

def _sort_ascending(key: SupportsLessThanT, value: SupportsLessThanT) -> bool:
	"""The compare function for ascending insertion sort"""
	
	return key < value


def _sort_descending(key: SupportsLessThanT, value: SupportsLessThanT) -> bool:
	"""The compare function for descending insertion sort"""
	
	return value < key


def move_to_place(sequence: MutableSequence[SupportsLessThanT],
                  key_index: int,
                  compare_func: Callable[[SupportsLessThanT,
                                          SupportsLessThanT], bool]) -> None:
	"""Insert sequence[key_index] into the sorted subarray
	sequence[: key_index]."""

	key = sequence[key_index]
	j = key_index - 1
	while j >= 0 and compare_func(key, sequence[j]):
		sequence[j + 1] = sequence[j]
		j -= 1
	sequence[j + 1] = key


def insertion_sort_recursive(sequence: MutableSequence[SupportsLessThanT],
                             n: int,
                             ascending: bool = True) -> None:
	"""You can also think of insertion sort as a recursive algorithm. In order
	to sort A[0: n], recursively sort the subarray A[0: n – 1] and then
	insert A[n] into the sorted subarray A[0 : n – 1]."""
	
	if ascending:
		compare_func = _sort_ascending
	else:
		compare_func = _sort_descending
	
	def _insertion_sort_recursive(_sequence: MutableSequence[SupportsLessThanT],
	                              _n: int) -> None:
		_n -= 1
	
		if _n < 1:
			return
		
		_insertion_sort_recursive(_sequence, _n)
	
		move_to_place(_sequence, _n, compare_func)
	
	_insertion_sort_recursive(sequence, n)


def insertion_sort(sequence: MutableSequence[SupportsLessThanT],
                   n: int,
                   ascending: bool = True) -> None:
	"""Sorts the first n items in sequence ascending (if increasing=True) else
	descending."""
	
	if ascending:
		compare_func = _sort_ascending
	else:
		compare_func = _sort_descending
	
	def _insertion_sort(_sequence: MutableSequence[SupportsLessThanT],
	                    _n: int) -> None:
		
		for i in range(1, _n):
			move_to_place(_sequence, i, compare_func)

	_insertion_sort(sequence, n)


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


def is_sorted(sequence: Sequence[SupportsLessThanT],
              ascending: bool = True) -> bool:
	"""Return True if sequence is sorted (ascending), else False."""
	
	if ascending:
		compare_operator = operator.le
	else:
		compare_operator = operator.ge

	return all(compare_operator(a, b)
	           for (a, b) in pairwise(sequence))


if __name__ == "__main__":
 
	def main() -> None:
		"""Driver code."""

		functions = (insertion_sort, insertion_sort_recursive)
		for function in functions:
			for i in range(250):
				lst: list[int] = list(range(i))
				shuffle(lst)

				for x in range(-1, 8):
					if x in lst:
						assert _linear_search(lst, len(lst), x) == lst.index(x)
					else:
						assert _linear_search(lst, len(lst), x) is None

				function(lst, len(lst))
				assert is_sorted(lst)

				function(lst, len(lst), ascending=False)
				assert is_sorted(lst, ascending=False)


	def average_case() -> None:
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

		assert f"{(n + 1) / 2:.2f}" == f"{items_tested/nr_tests:.2f}"
	
	def worst_case() -> None:
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

	main()
	average_case()
	worst_case()
