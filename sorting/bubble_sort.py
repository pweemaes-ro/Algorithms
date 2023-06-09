"""Yet another sorting algorithm..."""
from operator import lt, gt
from collections.abc import MutableSequence, Callable
from typing import Optional

from common import SupportsLessThanT


def bubble_sort(sequence: MutableSequence[SupportsLessThanT],
                key: Optional[Callable[[SupportsLessThanT],
                              SupportsLessThanT]] = None,
				reverse: bool = False) -> None:
	"""Inefficient but 'popular'... And stable."""

	if reverse:
		compare_operator = lt
	else:
		compare_operator = gt

	n = len(sequence)

	if key:
		keys: MutableSequence[SupportsLessThanT] = [*map(key, sequence)]
	else:
		keys = sequence

	for i in range(n - 1):
		no_swaps = True
		j = n - 1
		
		while j > i:
			if compare_operator(keys[j - 1], keys[j]):
				sequence[j], sequence[j - 1] = sequence[j - 1], sequence[j]
				if keys is not sequence:
					keys[j], keys[j - 1] = keys[j - 1], keys[j]
				no_swaps = False
			j -= 1

		if no_swaps:
			break
