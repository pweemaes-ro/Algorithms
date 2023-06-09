"""Another sorting algorithm..."""
from collections.abc import MutableSequence, Callable
from operator import gt, lt
from typing import Optional

from common import SupportsLessThanT


def selection_sort(sequence: MutableSequence[SupportsLessThanT],
                   key: Optional[Callable[[SupportsLessThanT],
                                 SupportsLessThanT]] = None,
                   reverse: bool = False) -> None:
	"""In place NON-STABLE sorting algorithm. Not very efficient, use merge
	sort!"""
	
	# Note: selection_sort is UNSTABLE by nature, and attempting to make it
	# stable would transform it in another sorting algorithm (say, insertion
	# sort).

	n = len(sequence)

	if reverse:
		compare_operator = gt
	else:
		compare_operator = lt
	
	if key:
		keys: MutableSequence[SupportsLessThanT] = [*map(key, sequence)]
	else:
		keys = sequence
	
	for i in range(n - 1):
		s = i
		for j in range(i + 1, n):
			if compare_operator(keys[j], keys[s]):
				s = j
		sequence[s], sequence[i] = sequence[i], sequence[s]
		if keys is not sequence:
			keys[s], keys[i] = keys[i], keys[s]
