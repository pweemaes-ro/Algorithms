"""Not suitable for large sequences..."""
from collections.abc import Callable
from random import randint
from typing import MutableSequence, Optional, Protocol, Any

from common import SupportsLessThanT
from key_functions import identity_key


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


def insertion_sort_recursive(sequence: MutableSequence[SupportsLessThanT],
                             key: Optional[Callable[..., Any]] = None,
                             reverse: bool = False) -> None:
	"""You can also think of insertion sort as a recursive algorithm. In order
	to sort A[0: n], recursively sort the subarray A[0: n – 1] and then
	insert A[n] into the sorted subarray A[0 : n – 1]."""

	if reverse:
		compare_func = _sort_descending
	else:
		compare_func = _sort_ascending
	
	key = key or identity_key
	
	def _insertion_sort_recursive(_sequence: MutableSequence[SupportsLessThanT],
	                              n: int) -> None:
		n -= 1
	
		if n < 1:
			return
		
		_insertion_sort_recursive(_sequence, n)
	
		_move_to_place(_sequence, n, compare_func, 0, len(sequence), key)
	
	_insertion_sort_recursive(sequence, len(sequence))


def _move_to_place(sequence: MutableSequence[SupportsLessThanT],
                   key_index: int,
                   compare_func: Callable[[SupportsLessThanT,
                                             SupportsLessThanT], bool],
                   start: int,
                   stop: int,
                   key: Optional[Callable[..., Any]] = None) -> None:
	"""Insert sequence[key_index] into the sorted subarray
	sequence[: key_index]."""

	key = key or identity_key
	key_value = sequence[key_index]
	j = key_index

	while stop > j >= start + 1 and \
		compare_func(key(key_value), key(sequence[j - 1])):
			sequence[j] = sequence[j - 1]
			j -= 1
	
	sequence[j] = key_value


def insertion_sort(sequence: MutableSequence[SupportsLessThanT],
                   start: int = 0,
                   stop: Optional[int] = None,
                   key: Optional[Callable[..., Any]] = None,
                   reverse: bool = False) -> None:
	"""New version that supports sorting from start to stop locations."""
	
	if stop is None:
		stop = len(sequence)

	if reverse:
		compare_func = _sort_descending
	else:
		compare_func = _sort_ascending

	key = key or identity_key

	for i in range(start, stop):
		_move_to_place(sequence, i, compare_func, start, stop, key)


class InsertionSortProtocol(Protocol):
	"""Protocol for specifying the signature of insertion_sort function."""
	
	def __call__(self,
	             sequence: MutableSequence[SupportsLessThanT],
	             start: int = 0,
	             stop: Optional[int] = None,
	             key: Optional[Callable[..., Any]] = None,
	             reverse: bool = False
	             ) -> None:
		...


class InsertionSortRecursiveProtocol(Protocol):
	"""Protocol for specifying the signature of insertion_sort_recursive
	function."""
	
	def __call__(self,
	             sequence: MutableSequence[SupportsLessThanT],
	             key: Optional[Callable[..., Any]] = None,
	             reverse: bool = False) -> None:
		...


def _test_insertion_sort(sort_function: InsertionSortProtocol |
                                        InsertionSortRecursiveProtocol) -> None:
	"""Do some tests for the sort_function..."""
	
	def mod_3(x: int) -> int:
		"""Just a test key function """
		
		return x % 3
	
	for i in range(25):
		base_lst = [randint(-i, i) for _ in range(i)]
		for key in (None, abs, mod_3):
			for reverse in (True, False):
				lst = list(base_lst)
				sort_function(lst, key=key, reverse=reverse)
				py_sorted = sorted(lst, key=key, reverse=reverse)
				assert py_sorted == lst
				print(f"{reverse=}, {key=}, {lst}")


def test_insertion_sort() -> None:
	"""Calls the real tests in a loop, with functions to test as argument..."""

	# The signatures of the functions, and the protocols used to specify these
	# signratures:
	#
	# def insertion_sort_recursive(sequence: MutableSequence[SupportsLessThanT],
	#                              reverse: bool = False) -> None:
	#
	# def insertion_sort(sequence: MutableSequence[SupportsLessThanT],
	#                    start: int = 0,
	#                    stop: Optional[int] = None,
	#                    reverse: bool = False) -> None:
	#
	# def _test_insertion_sort(sort_function: InsertionSortProtocol |
	#                                         InsertionSortRecursiveProtocol) \
	#       -> None:
	#
	# class InsertionSortProtocol(Protocol):
	# 	"""Protocol for specifying the signature of insertion_sort function."""
	#
	# 	def __call__(self,
	# 	             sequence: MutableSequence[SupportsLessThanT],
	# 	             start: int = 0,
	# 	             stop: Optional[int] = None,
	# 	             reverse: bool = False
	# 	             ) -> None:
	# 		...
	#
	# class InsertionSortRecursiveProtocol(Protocol):
	# 	"""Protocol for specifying the signature of insertion_sort_recursive
	#      function."""
	#
	# 	def __call__(self,
	# 	             sequence: MutableSequence[SupportsLessThanT],
	# 	             reverse: bool = False) -> None:
	# 		...
	#

	# for sort_function in (insertion_sort_recursive, insertion_sort):
	# 	# Mypy reports in the next line:
	# 	# error: Argument 1 to "_test_insertion_sort" has incompatible type
	# 	# "function"; expected "Union[InsertionSortProtocol,
	# 	# InsertionSortRecursiveProtocol]"
	# 	_test_insertion_sort(sort_function)

	# The following two lines are fine with Mypy! They are functionally
	# equivalent with the for-loop above...
	_test_insertion_sort(insertion_sort)
	_test_insertion_sort(insertion_sort_recursive)


if __name__ == "__main__":
	
	def _main() -> None:
		test_insertion_sort()

	_main()
