"""Test(s) for bubble_sort."""
from __future__ import annotations
from functools import lru_cache
from operator import attrgetter, itemgetter
from random import randint

from bubble_sort import bubble_sort


def test_bubble_sort() -> None:
	"""Test the merge sort ('Introduction to Algorithm' version)."""
	
	@lru_cache
	def is_odd(x: int) -> int:
		"""key function to sort by odd/even."""
		
		return x % 2
	
	class Sortable:
		"""A simple sortable class to test 'attrgetter' key."""
		
		def __init__(self, key_value: int):
			self.key_value = key_value
			self.derived = key_value % 3
		
		def __lt__(self, other: Sortable) -> bool:
			if isinstance(other, type(self)):
				return self.key_value < other.key_value
			else:
				raise NotImplementedError
		
		def __repr__(self) -> str:
			return f"({self.key_value}, {self.derived})"
	
	for i in range(100):
		base_lst = [randint(-i, i) for _ in range(i)]
		for reverse in (False, True):
			for key in (None, abs, is_odd):
				lst = list(base_lst)
				bubble_sort(lst, reverse=reverse, key=key)
				# bubble_sort is stable sort!
				assert lst == sorted(lst, reverse=reverse, key=key)
			
			attrgetter_key = attrgetter('derived')
			attrgetter_list = [Sortable(randint(-i, i)) for _ in range(i)]
			bubble_sort(attrgetter_list, key=attrgetter_key, reverse=reverse)
			# bubble_sort is stable sort!
			assert attrgetter_list == sorted(attrgetter_list,
			                                 key=attrgetter_key,
			                                 reverse=reverse)
			
			itemgetter_key = itemgetter(1)
			itemgetter_list = [(x := randint(-i, i), x % 3) for _ in range(i)]
			bubble_sort(itemgetter_list, key=itemgetter_key, reverse=reverse)
			# bubble_sort is stable sort!
			assert itemgetter_list == sorted(itemgetter_list,
			                                 key=itemgetter_key,
			                                 reverse=reverse)
