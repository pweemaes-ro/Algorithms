"""Not suitable for large sequences..."""
from itertools import pairwise
from random import shuffle
from typing import MutableSequence, Sequence, TypeVar, Optional, Literal

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


def insertion_sort(sequence: MutableSequence[SupportsLessThanT],
                   n: int,
                   ascending: bool = True) -> None:
	"""Sorts the first n items in sequence ascending (if increasing=True) else
	descending."""
	
	if ascending:
		compare_func = _sort_ascending
	else:
		compare_func = _sort_descending
	for i in range(1, n):
		key = sequence[i]
		# Insert sequence[i] into the sorted subarray sequence[: i].
		j = i - 1
		while j >= 0 and compare_func(key, sequence[j]):
			sequence[j + 1] = sequence[j]
			j -= 1
		sequence[j + 1] = key


T = TypeVar("T")

items_tested = 0

def linear_search_again(sequence: Sequence[T], n: int, key: T) -> Optional[int]:
	"""Return the index of the first occurance of x, or None if not found."""
	global items_tested
	i = 0
	while i < n:
		items_tested += 1
		if sequence[i] == key:  # Average: (n + 1) / 2 times, worst case: n times
			return i
		i += 1
	return None

# Qyestions about linear_search:
# 1. How many elements of Sequence need to be checked on the average, assuming
#    that the key is equailly likely to be any element in the Sequence?
# 2. How about the worst case?
# 3. Using Theta notation, give the average case and worst case runtimes
# JUSTIFY YOUR ANSWERS!
#
# ANSWERS:
# 1. If the key is the first item, 1 item is checked.
#    If the key is the second item, 2 items are checked.
#    ...
#    If the key is the last item, n items are checked.
#    Since each is equally likely, we have that the average nr of items checked
#    is sum(1 to n) / n = ((n * (n+1)) / 2) / n = (n + 1) / 2.
#    THIS IS VERIFIED BY average_case() function below.
# 2. Worst case is when the key is NOT in the sequence. Then all n items are
#    checked.
#    THIS IS VERIFIED BY worst_case() function below.
# 3. Both average and worst case are O(n). This follows from the fact that the
#    nr of times the item test is executed is linear in both cases. This is in
#    fact the only factor determining the execution time's dependency on n.
#
# Notice that in the best case, the first item is the key, and then the test
# is executed exactly 1 time, so best case is constant time O(1).

def __bin_to_int(binary: Sequence[int], n: int) -> int:
	return sum(binary[i] * 2 ** i for i in range(n))


def __int_to_bin(integer: int, n: int) -> MutableSequence[Literal[0, 1]]:
	"""Notice that in the returned sequence item 0 represents the LSB!"""
	
	bin_rep: MutableSequence[Literal[0, 1]] \
		= [1 if (integer & (2 ** i)) else 0 for i in range(n)]
	return bin_rep


def binary_add(value_1: Sequence[Literal[0, 1]],
               value_2: Sequence[Literal[0, 1]], n: int) \
	-> Sequence[Literal[0, 1]]:
	"""Adds value_1 to value_2."""

	a = __bin_to_int(value_1, n)
	print(f"{a=}")
	b = __bin_to_int(value_2, n)
	print(f"{b=}")
	c_binary = __int_to_bin(a + b, n + 1)
	assert a + b == __bin_to_int(c_binary, n + 1)
	return c_binary


def verify_sorted(sequence: Sequence[SupportsLessThanT]) -> bool:
	return all(a < b or a == b for (a, b) in pairwise(sequence))

def merge_ita(sequence: MutableSequence[SupportsLessThanT],
              start: int,
              middle: int,
              stop: int) \
	-> None:
	"""In place merge based on 'Introduction to Algorithms'"""

	left = sequence[start: middle]
	right = sequence[middle: stop]

	len_left = len(left)
	len_right = len(right)
	
	left_offset = right_offset = 0
	destination_offset = start
	
	while left_offset < len_left and right_offset < len_right:
		left_value = left[left_offset]
		right_value = right[right_offset]
		
		if left_value < right_value:
			sequence[destination_offset] = left_value
			left_offset += 1
		else:
			sequence[destination_offset] = right_value
			right_offset += 1
		
		destination_offset += 1
	
	while left_offset < len_left:
		sequence[destination_offset] = left[left_offset]
		left_offset += 1
		destination_offset += 1
	
	while right_offset < len_right:
		sequence[destination_offset] = right[right_offset]
		right_offset += 1
		destination_offset += 1
	

def merge_sort_ita(sequence: MutableSequence[SupportsLessThanT],
                   start: int = 0,
                   stop: Optional[int] = None,
                   level: int = 0) -> None:
	"""The in place merge sort based upon 'Introduction to Algorithms'"""
	
	if stop is None:
		stop = len(sequence)

	if stop - start <= 1:
		return

	middle = (stop + start) // 2

	merge_sort_ita(sequence, start, middle, level + 1)
	merge_sort_ita(sequence, middle, stop, level + 1)
	
	merge_ita(sequence, start, middle, stop)

lst: list[int] = []
print(lst)
merge_sort_ita(lst)
print(lst)

lst = [0]
print(lst)
merge_sort_ita(lst)
print(lst)

lst = [2, 1]
print(lst)
merge_sort_ita(lst)
print(lst)

lst = [12, 3, 7, 9, 14, 6, 11, 2]
print(lst)
merge_sort_ita(lst)
print(lst)

lst = [12, 3, 7, 9, 0, 14, 6, 11, 2]
print(lst)
merge_sort_ita(lst)
print(lst)
exit(0)


if __name__ == "__main__":
 
	def main() -> None:
		"""Driver code."""
		
		lst: list[int] = [5, 2, 4, 6, 1, 3]
		print(lst)
		insertion_sort(lst, len(lst))
		print(lst)
		insertion_sort(lst, len(lst), ascending=False)
		print(lst)
		for x in range(-1, 8):
			print(f"{x} found at index {linear_search_again(lst, len(lst), x)}")
	
		# NOTICE: FORMAT IS UNUSUAL, since MSB is bit 0!
		#                           1 + 4 + 8 + 32 + 64 + 128 = 245
		v_1: list[Literal[0, 1]] = [1, 0, 1, 0, 1, 1, 1, 1]
		#                           1 + 2 + 4 + 8 + 32 = 47
		v_2: list[Literal[0, 1]] = [1, 1, 1, 1, 0, 1, 0, 0]
		assert len(v_1) == len(v_2)
		add_result = binary_add(v_1, v_2, len(v_1))
		print(f"a+b={__bin_to_int(binary_add(v_1, v_2, len(v_1)), len(add_result))}")
	# main()
	
	def average_case() -> None:
		global items_tested
		items_tested = 0
		nr_tests = 500000
		n = 10
		print(f"Average case nr of items tested in linear_search "
		      f"({nr_tests = }, {n = }):")
		for i in range(nr_tests):
			lst = list(range(n))
			shuffle(lst)
			linear_search_again(lst, n, 0)
		
		print(f"Expected avg = (n + 1) / 2 = {(n + 1) / 2:.2f}")
		print(f"Counted avg                = {items_tested/nr_tests:.2f}")
	
	
	def worst_case() -> None:
		global items_tested
		items_tested = 0
		nr_tests = 500000
		n = 10
		print(f"Worst case nr of items tested in linear_search "
		      f"({nr_tests = }, {n = }):")
		for i in range(nr_tests):
			lst = list(range(n))
			shuffle(lst)
			linear_search_again(lst, n, -1)
		
		print(f"Expected avg = n = {n:.2f}")
		print(f"Counted avg      = {items_tested/nr_tests:.2f}")
	
	
	average_case()
	worst_case()


