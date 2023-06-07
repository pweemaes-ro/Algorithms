"""Another sorting algorithm..."""
from collections.abc import MutableSequence, Callable
from operator import gt, lt
from random import randint
from typing import Optional, Any

from common import SupportsLessThanT
from key_functions import identity_key
from tools import is_sorted


def selection_sort(unsorted: MutableSequence[SupportsLessThanT],
                   key: Optional[Callable[..., Any]] = None,
                   reverse: bool = False) -> None:
	"""In place NON-STABLE sorting algorithm. Not very efficient, use merge
	sort!"""
	
	n = len(unsorted)
	
	if reverse:
		compare_operator = gt
	else:
		compare_operator = lt
	
	key = key or identity_key
	
	for i in range(n - 1):
		s = i
		for j in range(i + 1, n):
			if compare_operator(key(unsorted[j]), key(unsorted[s])):
				s = j
		unsorted[s], unsorted[i] = unsorted[i], unsorted[s]


def test_selection_sort() -> None:
	"""Basic tests..."""
	
	def mod_3(n: int) -> int:
		"""Just a test key function """
		
		return n % 3
	
	for i in range(100):
		base_list = [randint(-i, i) for _ in range(i)]
		for reverse in (False, True):
			for key in (None, abs, mod_3):
				lst = list(base_list)
				selection_sort(lst, key=key, reverse=reverse)
				# selection_sort is NOT stable.
				assert is_sorted(lst, key, reverse), f"{key=}, {reverse=}, " \
				                                     f"{base_list=}."
	

if __name__ == "__main__":
	
	def _main() -> None:
		test_selection_sort()

	_main()
