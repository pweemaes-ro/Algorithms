"""Yet another sorting algorithm..."""
from operator import lt, gt
from collections.abc import MutableSequence, Callable
from typing import Any, Optional

from common import SupportsLessThanT


def bubble_sort(sequence: MutableSequence[SupportsLessThanT],
                key: Optional[Callable[..., Any]] = None,
				reverse: bool = False) -> None:
	"""Inefficient but 'popular'... And stable. """
	if reverse:
		compare_operator = lt
	else:
		compare_operator = gt

	n = len(sequence)

	keys: MutableSequence[SupportsLessThanT]

	if key:
		keys = [*map(key, sequence)]
	else:
		keys = sequence

	for i in range(n - 1):
		no_swaps = True
		j = n - 1
		
		while j > i:
			cmp_result = compare_operator(keys[j - 1],
			                              keys[j])

			if cmp_result:
				sequence[j], sequence[j - 1] = sequence[j - 1], sequence[j]
				if keys is not sequence:
					keys[j], keys[j - 1] = keys[j - 1], keys[j]
				no_swaps = False
			j -= 1

		if no_swaps:
			break


# MOVED TO tests/test_bubble_sort.py:
#
# def test_bubble_sort() -> None:
# 	"""Test the merge sort ('Introduction to Algorithm' version)."""
#
# 	from random import randint
#
# 	@lru_cache
# 	def is_odd(x: int) -> int:
# 		"""key function to sort by odd/even."""
# 		return x % 2
#
# 	class Sortable:
# 		"""A simple sortable class to test 'attrgetter' key."""
#
# 		def __init__(self, key_value: int):
# 			self.key_value = key_value
# 			self.derived = key_value % 3
#
# 		def __lt__(self, other: Any) -> bool:
# 			if isinstance(other, type(self)):
# 				return self.key_value < other.key_value
# 			else:
# 				raise NotImplementedError
#
# 		def __repr__(self) -> str:
# 			return f"({self.key_value}, {self.derived})"
#
# 	for i in range(100):
# 		base_lst = [randint(-i, i) for _ in range(i)]
# 		for reverse in (False, True):
# 			for key in (None, abs, is_odd):
# 				lst = list(base_lst)
# 				bubble_sort(lst, reverse=reverse, key=key)
# 				# bubble_sort is stable sort!
# 				assert lst == sorted(lst, reverse=reverse, key=key)
#
# 			attrgetter_key = attrgetter('derived')
# 			attrgetter_list = [Sortable(randint(-i, i)) for _ in range(i)]
# 			bubble_sort(attrgetter_list, reverse=reverse, key=attrgetter_key)
# 			# bubble_sort is stable sort!
# 			assert attrgetter_list == sorted(attrgetter_list,
# 			                                 reverse=reverse,
# 			                                 key=attrgetter_key)
#
# 			itemgetter_key = itemgetter(1)
# 			itemgetter_list = [(x := randint(-i, i), x % 3) for _ in range(i)]
# 			bubble_sort(itemgetter_list, reverse=reverse, key=itemgetter_key)
# 			# bubble_sort is stable sort!
# 			assert itemgetter_list == sorted(itemgetter_list,
# 			                                 reverse=reverse,
# 			                                 key=itemgetter_key)
