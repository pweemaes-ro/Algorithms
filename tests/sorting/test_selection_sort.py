"""Test(s) for selection_sort."""

from random import randint

from selection_sort import selection_sort
from tools import is_sorted


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
