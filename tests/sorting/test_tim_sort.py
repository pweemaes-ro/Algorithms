"""Test(s) for tim_sort."""
from random import randint

from tim_sort import tim_sort


def test_tim_sort() -> None:
	def mod_3(n: int) -> int:
		"""Just a test key function """
		
		return n % 3
	
	for i in range(500):
		base_lst = [randint(-i, i) for _ in range(i)]
		for key in (None, abs, mod_3):
			for reverse in (False, True):
				lst = list(base_lst)
				tim_sort(lst, key=key, reverse=reverse)
				assert lst == sorted(list(base_lst), key=key, reverse=reverse)
