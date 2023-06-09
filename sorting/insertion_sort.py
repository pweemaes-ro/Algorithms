"""Not suitable for large sequences..."""
from collections.abc import Callable
from operator import lt, gt
from typing import MutableSequence, Optional, Any

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


def insertion_sort_recursive(sequence: MutableSequence[SupportsLessThanT],
                             key: Optional[Callable[..., Any]] = None,
                             reverse: bool = False) -> None:
	"""You can also think of insertion sort as a recursive algorithm. In order
	to sort A[0: n], recursively sort the subarray A[0: n – 1] and then
	insert A[n] into the sorted subarray A[0 : n – 1]."""

	if reverse:
		compare_func = gt
	else:
		compare_func = lt
	
	keys: MutableSequence[SupportsLessThanT]

	if key:
		keys = [*map(key, sequence)]
	else:
		keys = sequence
	
	def _insertion_sort_recursive(_sequence: MutableSequence[SupportsLessThanT],
	                              n: int) -> None:
		n -= 1
		if n < 1:
			return
		
		_insertion_sort_recursive(_sequence, n)
	
		_move_to_place(_sequence, n, compare_func, 0, len(sequence), keys)
	
	_insertion_sort_recursive(sequence, len(sequence))


def _move_to_place(sequence: MutableSequence[SupportsLessThanT],
                   key_index: int,
                   compare_func: Callable[[SupportsLessThanT,
                                             SupportsLessThanT], bool],
                   start: int,
                   stop: int,
                   keys: MutableSequence[SupportsLessThanT]) -> None:
	"""Insert sequence[key_index] into the sorted subarray
	sequence[: key_index]."""

	key_item = sequence[key_index]
	key = keys[key_index]
	j = key_index

	while stop > j >= start + 1 and \
		compare_func(key, keys[j - 1]):
			sequence[j] = sequence[j - 1]
			if keys is not sequence:
				keys[j] = keys[j - 1]
			j -= 1
	
	sequence[j] = key_item
	if keys is not sequence:
		keys[j] = key


def insertion_sort(sequence: MutableSequence[SupportsLessThanT],
                   start: int = 0,
                   stop: Optional[int] = None,
                   key: Optional[Callable[..., Any]] = None,
                   reverse: bool = False) -> None:
	"""New version that supports sorting from start to stop locations."""
	
	if stop is None:
		stop = len(sequence)

	if reverse:
		compare_func = gt
	else:
		compare_func = lt

	keys: MutableSequence[SupportsLessThanT]

	if key:
		keys = [*map(key, sequence)]
	else:
		keys = sequence

	for i in range(start, stop):
		_move_to_place(sequence, i, compare_func, start, stop, keys)
