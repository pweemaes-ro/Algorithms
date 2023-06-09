"""Test(s) for merge_sort."""

from random import randint

from merge_sort import merge_sort


def test_merge_sort() -> None:
	"""Test the merge sort algorithm"""
	
	def mod_3(n: int) -> int:
		"""Just a test key function """
		
		return n % 3
	
	for i in range(500):
		base_lst = [randint(-i, i) for _ in range(i)]
		for key in (None, abs, mod_3):
			for reverse in (False, True):
				lst = list(base_lst)
				merge_sort(lst, key, reverse)
				# Merge sort is stable sort
				assert lst == sorted(lst, key=key, reverse=reverse)
